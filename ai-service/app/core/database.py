"""
Database Connection Manager and Async Session Factory.
Supports PostgreSQL (with pgvector) and transparent SQLite fallback for offline/isolated unit testing.
"""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.core.config import settings
from app.core.models import Base

engine = None
AsyncSessionLocal = None
_db_is_sqlite_fallback = False

async def init_database_engine():
    global engine, AsyncSessionLocal, _db_is_sqlite_fallback
    
    db_url = settings.DATABASE_URL
    try:
        # Attempt connecting to primary PostgreSQL engine
        test_engine = create_async_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        async with test_engine.connect() as conn:
            # Enable pgvector extension in Postgres if available
            try:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                await conn.commit()
            except Exception:
                pass
            await conn.execute(text("SELECT 1;"))
        
        engine = test_engine
        AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        _db_is_sqlite_fallback = False
        print(f"[Database] Successfully connected to PostgreSQL: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    except Exception as e:
        print(f"[Database] Notice: PostgreSQL not accessible ({e}). Initializing in-memory fallback engine for offline execution.")
        fallback_url = "sqlite+aiosqlite:///:memory:"
        engine = create_async_engine(fallback_url, echo=False)
        AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        _db_is_sqlite_fallback = True

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("[Database] Schema tables initialized.")

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        await init_database_engine()
    
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
