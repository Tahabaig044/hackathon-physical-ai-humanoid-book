import openai
from typing import List
from config import settings

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

class EmbeddingService:
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model

    async def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a single text"""
        try:
            response = await openai.Embedding.acreate(
                input=text,
                model=self.model
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return []

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = await self.create_embedding(text)
            embeddings.append(embedding)
        return embeddings

# Create a global instance
embedding_service = EmbeddingService()