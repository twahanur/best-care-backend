import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "Enterprise Car Rental Production Agentic RAG Microservice"
    VERSION: str = "2.0.0"
    API_PREFIX: str = ""
    HOST: str = os.getenv("AI_SERVICE_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("AI_SERVICE_PORT", "8000"))
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/digitalpylot_db"
    )
    SQLITE_FALLBACK_URL: str = "sqlite+aiosqlite:///:memory:"
    
    # Google Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
    GEMINI_FALLBACK_MODELS: str = os.getenv(
        "GEMINI_FALLBACK_MODELS",
        "gemini-3.6-flash,gemini-3.5-flash,gemini-flash-latest,gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-flash-lite-latest"
    )
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
    EMBEDDING_VERSION: str = "v1"
    EMBEDDING_DIMENSION: int = 256  # Fallback semantic dimension, 768 for Gemini text-embedding-004
    
    # RAG Retrieval Parameters
    TOP_K_RETRIEVAL: int = 5
    FINAL_TOP_K: int = 5
    MAX_CANDIDATES: int = 20
    SIMILARITY_THRESHOLD: float = 0.25
    RRF_K: int = 60  # Reciprocal Rank Fusion constant
    MAX_RETRIEVAL_ITERATIONS: int = 2
    
    # Conversational Memory
    MAX_HISTORY_TURNS: int = 10
    
    # Background Workers
    BACKGROUND_WORKERS_COUNT: int = 2
    WORKER_POLL_INTERVAL: float = 0.5

settings = Settings()
