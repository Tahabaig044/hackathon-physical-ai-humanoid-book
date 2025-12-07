# RAG Backend API

Backend API for the Physical AI & Humanoid Robotics Textbook RAG system.

## Overview

This FastAPI application provides the backend services for the RAG (Retrieval-Augmented Generation) system, including:
- Authentication and user management
- Chat and conversation management
- Document search and retrieval
- Translation services
- Vector database integration with Qdrant

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (copy `.env.example` to `.env` and update values)

## Running the Server

```bash
cd rag-backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user
- `POST /auth/login` - Authenticate a user
- `POST /auth/logout` - Logout a user

### Chat
- `GET /chat/conversations` - Get user's conversations
- `POST /chat/conversations` - Create a new conversation
- `GET /chat/conversations/{id}` - Get a specific conversation
- `PUT /chat/conversations/{id}` - Update a conversation
- `DELETE /chat/conversations/{id}` - Delete a conversation
- `GET /chat/conversations/{id}/messages` - Get messages in a conversation
- `POST /chat/conversations/{id}/messages` - Add a message to a conversation

### Documents
- `POST /documents/search` - Search for documents
- `GET /documents/modules` - Get available modules
- `GET /documents/module/{id}/chapters` - Get chapters for a module

### Translation
- `POST /translate` - Translate text
- `POST /translate/batch` - Translate multiple texts

## Configuration

Update the `.env` file with your configuration:
- Database URLs
- Qdrant connection details
- OpenAI API key
- JWT secret key

## Development

This project follows FastAPI best practices and includes:
- Pydantic models for request/response validation
- Dependency injection for database connections
- Proper error handling
- Async support for I/O operations