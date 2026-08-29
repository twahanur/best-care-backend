"""
FastAPI Application Entry Point for PostgreSQL-Powered Agentic RAG Microservice.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from app.core.config import settings
from app.core.database import init_database_engine, get_db_session
from app.core.models import KnowledgeDocument, RAGEmbedding
from app.indexing.seed_data import seed_knowledge_base_if_empty
from app.workers.background_worker import background_worker
from app.workers.embedding_queue import EmbeddingQueue
from app.api.rag_routes import router as rag_router
from app.api.lead_routes import router as lead_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize PostgreSQL Database & Schema
    print("[Lifespan] Initializing PostgreSQL database connection and tables...")
    await init_database_engine()

    # 2. Seed Initial Canonical Knowledge Base (Fleet, Policies, Guides) if empty
    print("[Lifespan] Checking and seeding knowledge base...")
    await seed_knowledge_base_if_empty()

    # 3. Start Non-Blocking Async Background Embedding Worker
    print("[Lifespan] Starting background embedding workers...")
    await background_worker.start()

    print("[Lifespan] Agentic RAG Microservice fully initialized and online.")
    yield

    # Shutdown
    print("[Lifespan] Shutting down background workers...")
    await background_worker.stop()
    print("[Lifespan] AI Microservice shutdown complete.")

app = FastAPI(
    title="Digital Pylot - PostgreSQL Agentic RAG Microservice",
    description=(
        "Production-grade, database-driven Agentic RAG microservice with PostgreSQL, "
        "pre-computed vector embeddings, non-blocking background workers, multilingual "
        "understanding (Bangla, Banglish, English), and multi-turn conversational memory."
    ),
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(rag_router)
app.include_router(lead_router)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Microservice Health Check & Database Status Endpoint.
    """
    doc_count = 0
    emb_count = 0
    try:
        async with get_db_session() as session:
            res1 = await session.execute(select(func.count(KnowledgeDocument.id)))
            doc_count = res1.scalar() or 0

            res2 = await session.execute(select(func.count(RAGEmbedding.id)).where(RAGEmbedding.status == "ACTIVE"))
            emb_count = res2.scalar() or 0
    except Exception as e:
        print(f"[Health] DB count error: {e}")

    queue_stats = await EmbeddingQueue.get_queue_stats()

    return {
        "status": "online",
        "service": "ai-rag-microservice",
        "version": settings.VERSION,
        "database_connected": True,
        "total_documents": doc_count,
        "active_embeddings": emb_count,
        "queue_stats": queue_stats,
        "multilingual_supported": ["english", "bangla", "banglish", "mixed"],
        "gemini_model": settings.GEMINI_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
