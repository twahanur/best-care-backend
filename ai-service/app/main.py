"""
FastAPI Application Entry Point for AI & RAG Microservice.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.vector_store import vector_store
from app.api.rag_routes import router as rag_router
from app.api.lead_routes import router as lead_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Pre-initialize vector store and knowledge embeddings
    print("[Lifespan] Starting AI & RAG Microservice... Initializing Vector Index.")
    await vector_store.initialize()
    print("[Lifespan] Vector Index ready for high-speed retrieval.")
    yield
    print("[Lifespan] Shutting down AI Microservice.")

app = FastAPI(
    title="Digital Pylot - Car Rental AI & RAG Microservice",
    description=(
        "Production-grade AI microservice providing Vector-based Retrieval-Augmented Generation (RAG), "
        "Vehicle Matchmaking, and Automated Lead Qualification powered by Gemini 2.0 / 1.5 Flash."
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
    Microservice Health Check & Status Endpoint.
    """
    return {
        "status": "online",
        "service": "ai-rag-microservice",
        "version": settings.VERSION,
        "vector_store_initialized": vector_store.is_initialized,
        "indexed_documents": len(vector_store.documents),
        "gemini_model": settings.GEMINI_MODEL,
        "embedding_model": settings.EMBEDDING_MODEL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
