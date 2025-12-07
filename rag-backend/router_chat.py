from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from config import settings
from neon_client import neon_client
from qdrant_service import qdrant_service
from embeddings import embedding_service
from rag_service import rag_service

router = APIRouter(prefix="/chat", tags=["chat"])

class ConversationCreateRequest(BaseModel):
    title: Optional[str] = None

class ConversationUpdateRequest(BaseModel):
    title: str

class MessageCreateRequest(BaseModel):
    content: str
    role: str = "user"  # "user" or "assistant"

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    content: str
    role: str
    created_at: datetime

class ChatResponse(BaseModel):
    conversation_id: int
    message_id: int
    response: str

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(limit: int = 20, offset: int = 0):
    """Get list of user's conversations"""
    try:
        query = """
            SELECT id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC
            LIMIT $1 OFFSET $2
        """
        result = await neon_client.execute_query(query, limit, offset)

        conversations = []
        for row in result:
            conversations.append(ConversationResponse(
                id=row['id'],
                title=row['title'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ))

        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversations: {str(e)}")

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(conversation_data: ConversationCreateRequest):
    """Create a new conversation"""
    try:
        title = conversation_data.title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        query = """
            INSERT INTO conversations (title, created_at, updated_at)
            VALUES ($1, $2, $3)
            RETURNING id, title, created_at, updated_at
        """
        result = await neon_client.execute_query(
            query,
            title,
            datetime.utcnow(),
            datetime.utcnow()
        )

        if not result:
            raise HTTPException(status_code=500, detail="Failed to create conversation")

        row = result[0]
        return ConversationResponse(
            id=row['id'],
            title=row['title'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int):
    """Get a specific conversation"""
    try:
        query = """
            SELECT id, title, created_at, updated_at
            FROM conversations
            WHERE id = $1
        """
        result = await neon_client.execute_query(query, conversation_id)

        if not result:
            raise HTTPException(status_code=404, detail="Conversation not found")

        row = result[0]
        return ConversationResponse(
            id=row['id'],
            title=row['title'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversation: {str(e)}")

@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(conversation_id: int, conversation_data: ConversationUpdateRequest):
    """Update a conversation's title"""
    try:
        query = """
            UPDATE conversations
            SET title = $1, updated_at = $2
            WHERE id = $3
            RETURNING id, title, created_at, updated_at
        """
        result = await neon_client.execute_query(
            query,
            conversation_data.title,
            datetime.utcnow(),
            conversation_id
        )

        if not result:
            raise HTTPException(status_code=404, detail="Conversation not found")

        row = result[0]
        return ConversationResponse(
            id=row['id'],
            title=row['title'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update conversation: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    """Delete a conversation and all its messages"""
    try:
        # First delete all messages in the conversation
        delete_messages_query = "DELETE FROM messages WHERE conversation_id = $1"
        await neon_client.execute_command(delete_messages_query, conversation_id)

        # Then delete the conversation
        delete_conversation_query = "DELETE FROM conversations WHERE id = $1"
        result = await neon_client.execute_command(delete_conversation_query, conversation_id)

        if result != "DELETE 1":
            raise HTTPException(status_code=404, detail="Conversation not found")

        return {"message": "Conversation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: int, limit: int = 50, offset: int = 0):
    """Get messages for a specific conversation"""
    try:
        query = """
            SELECT id, conversation_id, content, role, created_at
            FROM messages
            WHERE conversation_id = $1
            ORDER BY created_at ASC
            LIMIT $2 OFFSET $3
        """
        result = await neon_client.execute_query(query, conversation_id, limit, offset)

        messages = []
        for row in result:
            messages.append(MessageResponse(
                id=row['id'],
                conversation_id=row['conversation_id'],
                content=row['content'],
                role=row['role'],
                created_at=row['created_at']
            ))

        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch messages: {str(e)}")

@router.post("/conversations/{conversation_id}/messages", response_model=ChatResponse)
async def create_message(conversation_id: int, message_data: MessageCreateRequest):
    """Create a new message in a conversation and get a response"""
    try:
        # First, verify that the conversation exists
        conv_query = "SELECT id FROM conversations WHERE id = $1"
        conv_result = await neon_client.execute_query(conv_query, conversation_id)
        if not conv_result:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Save the user's message
        insert_message_query = """
            INSERT INTO messages (conversation_id, content, role, created_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id
        """
        message_result = await neon_client.execute_query(
            insert_message_query,
            conversation_id,
            message_data.content,
            message_data.role,
            datetime.utcnow()
        )

        if not message_result:
            raise HTTPException(status_code=500, detail="Failed to save message")

        user_message_id = message_result[0]['id']

        # Get RAG response based on the user's message
        response_text = await rag_service.get_rag_response(message_data.content, conversation_id)

        # Save the assistant's response
        assistant_message_result = await neon_client.execute_query(
            insert_message_query,
            conversation_id,
            response_text,
            "assistant",
            datetime.utcnow()
        )

        if not assistant_message_result:
            raise HTTPException(status_code=500, detail="Failed to save assistant response")

        assistant_message_id = assistant_message_result[0]['id']

        # Update conversation's updated_at timestamp
        update_conv_query = "UPDATE conversations SET updated_at = $1 WHERE id = $2"
        await neon_client.execute_command(update_conv_query, datetime.utcnow(), conversation_id)

        return ChatResponse(
            conversation_id=conversation_id,
            message_id=assistant_message_id,
            response=response_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create message: {str(e)}")

@router.delete("/conversations/{conversation_id}/messages/{message_id}")
async def delete_message(conversation_id: int, message_id: int):
    """Delete a specific message"""
    try:
        query = "DELETE FROM messages WHERE id = $1 AND conversation_id = $2"
        result = await neon_client.execute_command(query, message_id, conversation_id)

        if result != "DELETE 1":
            raise HTTPException(status_code=404, detail="Message not found in conversation")

        return {"message": "Message deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete message: {str(e)}")