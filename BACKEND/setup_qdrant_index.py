import qdrant_client
from qdrant_client.http import models
import os
import sys

sys.path.append(os.getcwd())
from src.config.settings import settings

def setup_index():
    print("Setting up Qdrant index...")
    client = qdrant_client.QdrantClient(
        url=settings.qdrant_cluster_endpoint,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False
    )
    
    collection_name = "My-Book"
    
    try:
        print(f"Checking collection '{collection_name}'...")
        collections = client.get_collections()
        collection_names = [c.name for c in collections.collections]
        
        if collection_name not in collection_names:
            print(f"Collection '{collection_name}' does not exist. Creating it...")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=1024, # Assuming cohere embed-english-v3.0
                    distance=models.Distance.COSINE
                )
            )
        
        print(f"Creating payload index for 'book_id' in '{collection_name}'...")
        client.create_payload_index(
            collection_name=collection_name,
            field_name="book_id",
            field_schema=models.PayloadSchemaType.KEYWORD
        )
        print("Index created successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_index()
