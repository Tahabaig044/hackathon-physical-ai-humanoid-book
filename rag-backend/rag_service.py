import logging
from typing import List, Dict, Any
from openai import AsyncOpenAI
from config import settings
from qdrant_service import qdrant_service
from embeddings import embedding_service
from neon_client import neon_client

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class RAGService:
    def __init__(self):
        self.collection_name = "textbook_documents"

    async def get_rag_response(self, query: str, conversation_id: int = None) -> str:
        """
        Process user query, retrieve relevant documents, and generate response
        """
        try:
            # Create embedding for the query
            query_embedding = await embedding_service.create_embedding(query)

            # Search for relevant documents in Qdrant
            search_results = qdrant_service.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=5  # Retrieve top 5 most relevant documents
            )

            # Extract relevant context from search results
            context_parts = []
            for hit in search_results:
                payload = hit.payload
                text = payload.get("text", "")
                title = payload.get("title", "")
                source = payload.get("source", "")

                if text:
                    context_parts.append(f"Source: {title} ({source})\nContent: {text}\n")

            context = "\n".join(context_parts)

            # Prepare the prompt for the LLM
            if context:
                system_prompt = f"""
                You are an AI assistant for the Physical AI & Humanoid Robotics Textbook.
                Use the following context from the textbook to answer the user's question.
                If the context doesn't contain relevant information, say so and provide a general response based on your knowledge.
                Be helpful, accurate, and concise.

                Context:
                {context}
                """
            else:
                system_prompt = """
                You are an AI assistant for the Physical AI & Humanoid Robotics Textbook.
                Answer the user's question based on your general knowledge about robotics, AI, and related topics.
                Be helpful, accurate, and concise.
                """

            # Call the OpenAI API to generate a response
            response = await openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error in RAG service: {e}")
            return "I'm sorry, but I encountered an error while processing your request. Please try again later."

    async def ingest_document(self, title: str, content: str, source: str, module: str, chapter: str) -> bool:
        """
        Ingest a document into the vector database
        """
        try:
            # Create embedding for the content
            embedding = await embedding_service.create_embedding(content)

            # Prepare payload
            payload = {
                "title": title,
                "text": content,
                "source": source,
                "module": module,
                "chapter": chapter,
                "created_at": "TODO"  # Would be a timestamp in real implementation
            }

            # Upsert into Qdrant
            qdrant_service.upsert_vectors(
                collection_name=self.collection_name,
                vectors=[embedding],
                payload=[payload]
            )

            return True
        except Exception as e:
            logging.error(f"Error ingesting document: {e}")
            return False

    async def batch_ingest_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ingest multiple documents into the vector database
        """
        success_count = 0
        error_count = 0
        errors = []

        for doc in documents:
            try:
                success = await self.ingest_document(
                    title=doc.get("title", ""),
                    content=doc.get("content", ""),
                    source=doc.get("source", ""),
                    module=doc.get("module", ""),
                    chapter=doc.get("chapter", "")
                )
                if success:
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Error ingesting document '{doc.get('title', 'Unknown')}': {str(e)}")

        return {
            "total": len(documents),
            "success": success_count,
            "errors": error_count,
            "error_details": errors
        }

# Create a global instance
rag_service = RAGService()