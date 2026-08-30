from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.indexing.document_ingester import document_ingester
from app.api.routes import router as rag_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    print("[AI-Service] Starting Best Care AI & RAG Microservice...")
    try:
        await init_db()
        await document_ingester.seed_knowledge_base()
    except Exception as e:
        print(f"[AI-Service] Startup initialization notice: {e}")
    yield
    print("[AI-Service] Shutting down AI Microservice...")

app = FastAPI(
    title="Best Care Car Rental AI & RAG Service",
    description="Production-Ready Hybrid RAG and Conversational Booking Engine",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routes
app.include_router(rag_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "best-care-ai-rag-service", "version": "2.0.0"}

@app.get("/")
async def root():
    return {
        "service": "Best Care AI & RAG Service",
        "status": "operational",
        "endpoints": ["/rag/chat", "/rag/admin/chat", "/rag/documents", "/health"]
    }
