import qdrant_client
client = qdrant_client.QdrantClient(":memory:")
help(client.query_points)
