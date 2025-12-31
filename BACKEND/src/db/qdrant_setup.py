"""
Qdrant collection setup for vector storage
"""
import qdrant_client

from qdrant_client.http import models
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class QdrantSetup:
    def __init__(self):
        # Initialize Qdrant client
        self.client = qdrant_client.QdrantClient(
            url=os.getenv("QDRANT_CLUSTER_ENDPOINT", ""),
            api_key=os.getenv("QDRANT_API_KEY", ""),
            prefer_grpc=False  # Using HTTP for simplicity
        )
        
        # Cohere embeddings are 1024 dimensions for embed-english-v3.0
        self.vector_size = 1024
        self.collection_name = "book_content_chunks"
    
    def create_collection(self):
        """
        Create a collection for storing book content chunks with embeddings
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create the collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                
                # Create payload index for efficient filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="book_id",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )
                
                print(f"Collection '{self.collection_name}' created successfully.")
            else:
                print(f"Collection '{self.collection_name}' already exists.")
                
        except Exception as e:
            print(f"Error creating collection: {e}")
            raise
    
    def delete_collection(self):
        """
        Delete the collection (useful for development)
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting collection: {e}")
    
    def recreate_collection(self):
        """
        Delete and recreate the collection
        """
        self.delete_collection()
        self.create_collection()

# Example usage
if __name__ == "__main__":
    qdrant_setup = QdrantSetup()
    qdrant_setup.create_collection()
