import qdrant_client
try:
    print(f"File: {qdrant_client.__file__}")
except:
    print("No __file__")

try:
    client = qdrant_client.QdrantClient(":memory:")
    print("Attributes of client instance:", dir(client))
    if hasattr(client, 'search'):
        print("Has search")
    else:
        print("No search")
except Exception as e:
    print(f"Error initializing client: {e}")