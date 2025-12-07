from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import logging

from qdrant_service import models
from config import settings
from qdrant_service import QdrantClient
from embeddings import embedding_service

router = APIRouter(prefix="/documents", tags=["documents"])

# Initialize Qdrant client
qdrant_client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    api_key=settings.QDRANT_API_KEY
)

class DocumentSearchRequest(BaseModel):
    query: str
    limit: int = Query(10, ge=1, le=100)
    filters: Optional[dict] = None

class DocumentSearchResponse(BaseModel):
    results: List[dict]
    total: int

@router.post("/search", response_model=DocumentSearchResponse)
async def search_documents(request: DocumentSearchRequest):
    """
    Search for documents in the vector database based on the query
    """
    try:
        # Create embedding for the query
        query_embedding = await embedding_service.create_embedding(request.query)

        # Perform similarity search in Qdrant
        search_results = qdrant_client.search(
            collection_name="textbook_documents",  # Assuming this collection exists
            query_vector=query_embedding,
            limit=request.limit,
            query_filter=None if not request.filters else models.Filter(
                must=[models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                ) for key, value in request.filters.items()]
            )
        )

        # Format results
        results = []
        for hit in search_results:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
                "text": hit.payload.get("text", ""),
                "title": hit.payload.get("title", ""),
                "source": hit.payload.get("source", ""),
                "module": hit.payload.get("module", ""),
                "chapter": hit.payload.get("chapter", "")
            })

        return DocumentSearchResponse(
            results=results,
            total=len(results)
        )
    except Exception as e:
        logging.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during document search")

@router.get("/modules")
async def get_modules():
    """
    Get list of available modules in the textbook
    """
    try:
        # This would typically fetch from a database or predefined list
        modules = [
            {"id": "module1-ros2", "name": "Module 1: ROS 2"},
            {"id": "module2-gazebo-unity", "name": "Module 2: Gazebo & Unity"},
            {"id": "module3-nvidia-isaac", "name": "Module 3: NVIDIA Isaac"},
            {"id": "module4-vla", "name": "Module 4: Vision-Language-Action (VLA)"},
            {"id": "capstone", "name": "Capstone: Autonomous Humanoid"}
        ]
        return {"modules": modules}
    except Exception as e:
        logging.error(f"Error fetching modules: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/module/{module_id}/chapters")
async def get_chapters(module_id: str):
    """
    Get list of chapters for a specific module
    """
    try:
        # This would typically fetch from a database
        # For now, returning a predefined structure
        chapter_mapping = {
            "module1-ros2": [
                {"id": "introduction", "name": "Introduction to ROS 2"},
                {"id": "installation", "name": "ROS 2 Installation"},
                {"id": "basic-concepts", "name": "Basic Concepts"},
                {"id": "nodes-topics-services", "name": "Nodes, Topics, and Services"},
                {"id": "packages-workspaces", "name": "Packages and Workspaces"}
            ],
            "module2-gazebo-unity": [
                {"id": "introduction", "name": "Introduction to Gazebo & Unity"},
                {"id": "gazebo-basics", "name": "Gazebo Basics"},
                {"id": "unity-integration", "name": "Unity Integration"},
                {"id": "simulation-environments", "name": "Simulation Environments"},
                {"id": "physics-engines", "name": "Physics Engines"}
            ],
            "module3-nvidia-isaac": [
                {"id": "introduction", "name": "Introduction to NVIDIA Isaac"},
                {"id": "isaac-sdk", "name": "Isaac SDK"},
                {"id": "perception-systems", "name": "Perception Systems"},
                {"id": "navigation", "name": "Navigation"},
                {"id": "manipulation", "name": "Manipulation"}
            ],
            "module4-vla": [
                {"id": "introduction", "name": "Introduction to VLA"},
                {"id": "vision-systems", "name": "Vision Systems"},
                {"id": "language-understanding", "name": "Language Understanding"},
                {"id": "action-planning", "name": "Action Planning"},
                {"id": "integration", "name": "Integration"}
            ],
            "capstone": [
                {"id": "introduction", "name": "Introduction"},
                {"id": "system-architecture", "name": "System Architecture"},
                {"id": "integration", "name": "Integration"},
                {"id": "testing", "name": "Testing"},
                {"id": "future-directions", "name": "Future Directions"}
            ]
        }

        if module_id not in chapter_mapping:
            raise HTTPException(status_code=404, detail="Module not found")

        return {"chapters": chapter_mapping[module_id]}
    except Exception as e:
        logging.error(f"Error fetching chapters: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")