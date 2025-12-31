import qdrant_client
from qdrant_client.http import models

client = qdrant_client.QdrantClient(":memory:")
client.create_collection(
    collection_name="test",
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE)
)
client.upsert(
    collection_name="test",
    points=[
        models.PointStruct(id=1, vector=[0.1, 0.1, 0.1, 0.1], payload={"city": "London"}),
    ]
)

try:
    results = client.query_points(
        collection_name="test",
        query=[0.1, 0.1, 0.1, 0.1],
        limit=1
    )
    print("Result type:", type(results))
    print("Result dir:", dir(results))
    if hasattr(results, 'points'):
        print("Points:", results.points)
except Exception as e:
    print("Error:", e)
