import qdrant_client
client = qdrant_client.QdrantClient(":memory:")
print("query_points doc:")
print(client.query_points.__doc__)
print("-" * 20)
if hasattr(client, 'search'):
    print("search doc:")
    print(client.search.__doc__)
else:
    print("search missing")

print("-" * 20)
print("query doc:")
print(client.query.__doc__)
