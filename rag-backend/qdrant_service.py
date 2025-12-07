from qdrant_service import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
from config import settings

class QdrantService:
    def __init__(self):
        # Initialize Qdrant client
        if settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                api_key=settings.QDRANT_API_KEY
            )
        else:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )

    def create_collection(self, collection_name: str, vector_size: int = 1536):
        """Create a collection for storing document embeddings"""
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' created successfully")
        except Exception as e:
            print(f"Collection '{collection_name}' might already exist: {e}")

    def upsert_vectors(self, collection_name: str, vectors: List[Dict], payload: List[Dict]):
        """Upsert vectors into the collection"""
        points = [
            models.PointStruct(
                id=i,
                vector=vector,
                payload=payload[i]
            ) for i, vector in enumerate(vectors)
        ]

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

    def search(self, collection_name: str, query_vector: List[float], limit: int = 10):
        """Search for similar vectors in the collection"""
        results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return results

    def delete_collection(self, collection_name: str):
        """Delete a collection"""
        try:
            self.client.delete_collection(collection_name)
            print(f"Collection '{collection_name}' deleted successfully")
        except Exception as e:
            print(f"Error deleting collection '{collection_name}': {e}")

# Create a global instance
qdrant_service = QdrantService()