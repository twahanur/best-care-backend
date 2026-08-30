import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.core.models import Base

# Create Async Engine with NullPool for robust event loop compatibility with Neon PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=NullPool
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

async def init_db():
    """
    Initialize PostgreSQL extensions, drop obsolete RAG tables, and create new tables.
    """
    async with engine.begin() as conn:
        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        except Exception as e:
            print(f"[DB] Vector extension notice: {e}")

        legacy_tables = [
            "user_memories",
            "chat_messages",
            "chat_conversations",
            "embedding_jobs",
            "rag_embeddings",
            "rag_chunks",
            "rag_documents"
        ]
        for tbl in legacy_tables:
            try:
                await conn.execute(text(f"DROP TABLE IF EXISTS {tbl} CASCADE;"))
            except Exception as e:
                print(f"[DB] Notice dropping legacy table {tbl}: {e}")

        await conn.run_sync(Base.metadata.create_all)
        print("[DB] Initialized clean knowledge base and chat session tables successfully.")
