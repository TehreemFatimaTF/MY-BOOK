"""
QdrantService implementation for vector search
"""
import qdrant_client
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
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
            prefer_grpc=False  # Using HTTP for simplicity
        )
        
        self.collection_name = settings.qdrant_collection_name
    
    def search(
        self, 
        query_text: str, 
        book_id: Optional[str] = None, 
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant content chunks based on the query
        """
        try:
            # Generate embedding for the query
            query_embedding = cohere_embedding_service.embed_query(query_text)
            
            # Prepare filters
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
            
            # Perform search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=filters,
                limit=limit,
                score_threshold=threshold
            )
            
            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "content": hit.payload.get("chunk_text", ""),
                    "relevance_score": hit.score,
                    "book_id": hit.payload.get("book_id"),
                    "chunk_index": hit.payload.get("chunk_index"),
                    "start_pos": hit.payload.get("start_pos"),
                    "end_pos": hit.payload.get("end_pos")
                })
            
            logger.info(f"Qdrant search returned {len(results)} results for query: '{query_text[:50]}...'")
            return results
            
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {e}")
            raise ExternalServiceError("Qdrant", str(e))
    
    def search_with_selected_text(
        self, 
        selected_text: str, 
        query_text: str,
        book_id: str,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search using both selected text and query for more focused results
        """
        try:
            # Generate embedding for the combined query (selected text + query)
            combined_query = f"Selected text: {selected_text}\n\nQuestion about this text: {query_text}"
            query_embedding = cohere_embedding_service.embed_query(combined_query)
            
            # Prepare filters to only search within the specific book
            filters = models.Filter(
                must=[
                    models.FieldCondition(
                        key="book_id",
                        match=models.MatchValue(value=book_id)
                    )
                ]
            )
            
            # Perform search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=filters,
                limit=limit,
                score_threshold=0.3  # Lower threshold for selected text queries
            )
            
            # Format results
            results = []
            for hit in search_results:
                results.append({
                    "id": hit.id,
                    "content": hit.payload.get("chunk_text", ""),
                    "relevance_score": hit.score,
                    "book_id": hit.payload.get("book_id"),
                    "chunk_index": hit.payload.get("chunk_index"),
                    "start_pos": hit.payload.get("start_pos"),
                    "end_pos": hit.payload.get("end_pos")
                })
            
            logger.info(f"Qdrant search with selected text returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching in Qdrant with selected text: {e}")
            raise ExternalServiceError("Qdrant", str(e))
    
    def add_document_chunks(self, book_id: str, chunks: List[Dict[str, Any]]):
        """
        Add document chunks to the Qdrant collection
        """
        try:
            # Generate embeddings for all chunks
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = cohere_embedding_service.embed_text(chunk_texts)
            
            # Prepare points for insertion
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point = models.PointStruct(
                    id=f"{book_id}_chunk_{i}",
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
            
            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(points)} chunks to Qdrant for book {book_id}")
            
        except Exception as e:
            logger.error(f"Error adding document chunks to Qdrant: {e}")
            raise ExternalServiceError("Qdrant", str(e))
    
    def delete_book_chunks(self, book_id: str):
        """
        Delete all chunks associated with a specific book
        """
        try:
            # Create filter for the book
            book_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="book_id",
                        match=models.MatchValue(value=book_id)
                    )
                ]
            )
            
            # Delete points matching the filter
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=book_filter
                )
            )
            
            logger.info(f"Deleted all chunks for book {book_id} from Qdrant")
            
        except Exception as e:
            logger.error(f"Error deleting book chunks from Qdrant: {e}")
            raise ExternalServiceError("Qdrant", str(e))
    
    def check_collection_exists(self) -> bool:
        """
        Check if the collection exists
        """
        try:
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            return self.collection_name in collection_names
        except Exception as e:
            logger.error(f"Error checking if collection exists in Qdrant: {e}")
            return False

# Global instance
qdrant_service = QdrantService()