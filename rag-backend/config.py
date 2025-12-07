import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL", "")

    # Qdrant settings
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # JWT settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Application settings
    APP_NAME = os.getenv("APP_NAME", "RAG Backend")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()