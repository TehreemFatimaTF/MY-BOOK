import qdrant_client
import os
import sys

sys.path.append(os.getcwd())
from src.config.settings import settings

def check_count():
    print("Checking Qdrant count...")
    client = qdrant_client.QdrantClient(
        url=settings.qdrant_cluster_endpoint,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False
    )
    
    collection_name = "My-Book"
    try:
        count = client.count(collection_name=collection_name)
        print(f"Count for '{collection_name}': {count}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_count()
