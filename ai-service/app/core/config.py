import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    AI_SERVICE_HOST: str = os.getenv("AI_SERVICE_HOST", "0.0.0.0")
    AI_SERVICE_PORT: int = int(os.getenv("AI_SERVICE_PORT", "8000"))
    AI_SERVICE_ENV: str = os.getenv("AI_SERVICE_ENV", "production")
    BACKEND_GATEWAY_URL: str = os.getenv("BACKEND_GATEWAY_URL", "http://localhost:4000")

    # PostgreSQL Database URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://neondb_owner:npg_MHut8IFrl6Vq@ep-still-flower-ao4zszco-pooler.c-2.ap-southeast-1.aws.neon.tech/best_car?ssl=require"
    )

    # Google Gemini GenAI Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    GEMINI_FALLBACK_MODELS: str = os.getenv(
        "GEMINI_FALLBACK_MODELS",
        "gemini-2.0-flash,gemini-1.5-flash,gemini-1.5-flash-8b,gemini-2.0-flash-exp"
    )
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
    EMBEDDING_DIMENSION: int = 768

    # RAG Retrieval & Memory Tuning
    TOP_K_RETRIEVAL: int = 5
    MAX_HISTORY_TURNS: int = 10
    MAX_CONTEXT_CHARS: int = 4000

    @property
    def fallback_model_list(self) -> List[str]:
        return [m.strip() for m in self.GEMINI_FALLBACK_MODELS.split(",") if m.strip()]

    model_config = ConfigDict(extra="allow", case_sensitive=True)

settings = Settings()
