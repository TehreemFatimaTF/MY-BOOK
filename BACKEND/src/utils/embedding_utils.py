"""
Embedding utility functions for Cohere integration
"""
import cohere
from typing import List, Optional
from src.config.settings import settings
from src.utils.logging import logger, ExternalServiceError

class CohereEmbeddingService:
    def __init__(self):
        if not settings.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")
        
        self.client = cohere.Client(settings.cohere_api_key)
        self.model = settings.cohere_embedding_model
    
    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        try:
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # Using search_document for book content
            )
            
            if not response or not response.embeddings:
                raise ExternalServiceError("Cohere", "No embeddings returned from Cohere API")
            
            return response.embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings with Cohere: {e}")
            raise ExternalServiceError("Cohere", str(e))
    
    def embed_single_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        embeddings = self.embed_text([text])
        return embeddings[0] if embeddings else []
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query (using search_query input type)
        """
        try:
            response = self.client.embed(
                texts=[query],
                model=self.model,
                input_type="search_query"  # Using search_query for user queries
            )
            
            if not response or not response.embeddings:
                raise ExternalServiceError("Cohere", "No embeddings returned from Cohere API")
            
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating query embedding with Cohere: {e}")
            raise ExternalServiceError("Cohere", str(e))

# Global instance
cohere_embedding_service = CohereEmbeddingService()

# Example usage:
# embedding = cohere_embedding_service.embed_single_text("This is a sample text")
# print(f"Embedding length: {len(embedding)}")