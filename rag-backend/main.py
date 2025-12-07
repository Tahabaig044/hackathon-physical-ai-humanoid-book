from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router_auth import router as auth_router
from router_chat import router as chat_router
from router_docs import router as docs_router
from router_translation import router as translation_router

app = FastAPI(
    title="RAG Backend API",
    description="Backend API for Physical AI & Humanoid Robotics Textbook RAG system",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(docs_router)
app.include_router(translation_router)

@app.get("/")
def read_root():
    return {"message": "RAG Backend API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)