"""
QdrantService implementation for vector search - FIXED VERSION
"""
import qdrant_client
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import uuid  # UUID generation ke liye zaroori hai
from src.config.settings import settings
from src.utils.logging import logger, ExternalServiceError
from src.utils.embedding_utils import cohere_embedding_service

class QdrantService:
    def __init__(self):
        if not settings.qdrant_cluster_endpoint or not settings.qdrant_api_key:
            raise ValueError("QDRANT_CLUSTER_ENDPOINT and QDRANT_API_KEY environment variables must be set")
        
        # Initialize Qdrant client
        self.client = qdrant_client.QdrantClient(
            url=settings.qdrant_cluster_endpoint,
            api_key=settings.qdrant_api_key,
            prefer_grpc=False
        )
        
        # FIX: Dashboard ke mutabiq sahi collection name
        self.collection_name = "My-Book"
    
    def search(
        self, 
        query_text: str, 
        book_id: Optional[str] = None, 
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Search for relevant content chunks"""
        try:
            query_embedding = cohere_embedding_service.embed_query(query_text)
            
            filters = None
            if book_id:
                filters = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_id",
                            match=models.MatchValue(value=book_id)
                        )
                    ]
                )
            
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                query_filter=filters,
                limit=limit,
                score_threshold=threshold
            ).points
            
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "content": hit.payload.get("chunk_text", ""),
                    "relevance_score": hit.score,
                    "book_id": hit.payload.get("book_id"),
                    "chunk_index": hit.payload.get("chunk_index")
                })
            
            logger.info(f"Qdrant search returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {e}")
            raise ExternalServiceError("Qdrant", str(e))

    def add_document_chunks(self, book_id: str, chunks: List[Dict[str, Any]]):
        """Add document chunks with valid UUIDs and correct collection name"""
        try:
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = cohere_embedding_service.embed_text(chunk_texts)
            
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                # FIX: String "chunk_0" ki wajah se error aa raha tha, ab UUID use hoga
                point_id = str(uuid.uuid4()) 
                
                point = models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "book_id": book_id,
                        "chunk_text": chunk['text'],
                        "start_pos": chunk.get('start_pos', 0),
                        "end_pos": chunk.get('end_pos', 0),
                        "chunk_index": i
                    }
                )
                points.append(point)
            
            # Upload to 'My-Book'
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Added {len(points)} chunks to Qdrant collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error adding document chunks: {e}")
            raise ExternalServiceError("Qdrant", str(e))

    def delete_book_chunks(self, book_id: str):
        """Delete chunks for a specific book"""
        try:
            book_filter = models.Filter(
                must=[models.FieldCondition(key="book_id", match=models.MatchValue(value=book_id))]
            )
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(filter=book_filter)
            )
        except Exception as e:
            logger.error(f"Error deleting: {e}")
            raise

# Global instance
qdrant_service = QdrantService()
