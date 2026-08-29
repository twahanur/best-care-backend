"""
FastAPI Route Handlers for Database-Driven Agentic RAG, Multilingual Chat, Memory, and Dynamic Document Indexing.
"""
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy import select, delete
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument, RAGEmbedding, get_utc_now
from app.agent.rag_agent import rag_agent
from app.memory.conversation_memory import conversation_memory
from app.workers.embedding_queue import EmbeddingQueue
from app.indexing.canonical_builder import CanonicalBuilder
from app.indexing.change_detector import ChangeDetector

router = APIRouter(prefix="/rag", tags=["Agentic RAG & Knowledge Engine"])

# Request & Response Schemas
class AgentChatRequest(BaseModel):
    query: str = Field(..., examples=["What is the security deposit and refund timeline?"])
    session_id: Optional[str] = Field(None, examples=["session_custom_101"])
    user_id: Optional[str] = Field(None, examples=["user_123"])
    category: Optional[str] = Field(None, examples=["Rental Policy"])

class AgentChatResponse(BaseModel):
    session_id: str
    query: str
    answer: str
    language: str
    intent: Optional[str] = None
    sources: List[Dict[str, Any]]
    matched_vehicles: List[Dict[str, Any]]
    confidence_score: float

class LegacyRAGQueryRequest(BaseModel):
    query: str = Field(...)
    category: Optional[str] = None

class LegacyRAGQueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[Dict[str, Any]]
    matched_vehicles: List[Dict[str, Any]]

class CarRecommendRequest(BaseModel):
    trip_description: str = Field(..., examples=["Family trip of 6 people going to Sylhet tea gardens with lots of luggage"])
    passengers: int = Field(default=4, ge=1, le=15, examples=[6])
    budget_per_day: Optional[float] = Field(None, examples=[150.0])
    terrain: Optional[str] = Field(None, examples=["Hills / Off-road"])

class CreateDocumentRequest(BaseModel):
    id: str = Field(..., examples=["fleet_defender_v8"])
    entity_type: str = Field(default="vehicle", examples=["vehicle", "policy", "trip_guide", "faq"])
    category: str = Field(..., examples=["Fleet Specs", "Rental Policy"])
    title: str = Field(..., examples=["Land Rover Defender 110 (Off-Road Luxury)"])
    content: str = Field(..., examples=["Model: Defender 110. Daily Rate: $165. 7 Seats. 4WD."])
    tags: List[str] = Field(default=[], examples=[["suv", "luxury", "offroad", "defender"]])
    metadata: Dict[str, Any] = Field(default={}, examples=[{"dailyRate": 165, "seats": 7}])

# --- 1. Agentic Chat with Conversational Memory & Multilingual RAG ---
@router.post("/chat", response_model=AgentChatResponse)
async def handle_agent_chat(payload: AgentChatRequest):
    """
    Agentic Multi-Turn Chat: Answers in the perspective of previous turns, grounds against PostgreSQL pgvector database,
    and supports natural language in English, Bengali (বাংলা), and Banglish.
    """
    try:
        result = await rag_agent.chat(
            user_query=payload.query,
            session_id=payload.session_id,
            user_id=payload.user_id,
            category=payload.category
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agentic chat processing failed: {str(e)}")

@router.post("/query", response_model=LegacyRAGQueryResponse)
async def handle_rag_query(payload: LegacyRAGQueryRequest):
    """
    Grounded RAG Query (backward compatible).
    """
    try:
        res = await rag_agent.chat(user_query=payload.query, category=payload.category)
        return {
            "query": res["query"],
            "answer": res["answer"],
            "sources": res["sources"],
            "matched_vehicles": res["matched_vehicles"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query execution failed: {str(e)}")

# --- 2. AI Vehicle Matchmaker ---
@router.post("/recommend-car")
async def handle_car_recommendation(payload: CarRecommendRequest):
    """
    AI Matchmaker: Recommends optimal vehicles based on trip dynamics, group size, and terrain.
    """
    try:
        result = await rag_agent.recommend_vehicle(
            trip_description=payload.trip_description,
            passengers=payload.passengers,
            budget_per_day=payload.budget_per_day,
            terrain=payload.terrain
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Car recommendation failed: {str(e)}")

# --- 3. Session History & Memory Management ---
@router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """
    Retrieve message turns and context stored in memory for a conversation session.
    """
    history = await conversation_memory.get_history(session_id)
    return {
        "session_id": session_id,
        "total_turns": len(history),
        "history": history
    }

@router.delete("/sessions/{session_id}")
async def clear_session_history(session_id: str):
    """
    Clear session memory.
    """
    await conversation_memory.clear_history(session_id)
    return {"status": "cleared", "session_id": session_id}

# --- 4. Dynamic PostgreSQL Knowledge Documents CRUD ---
@router.get("/documents")
@router.get("/knowledge-docs")
async def get_knowledge_documents():
    """
    Inspect all active documents in PostgreSQL knowledge base.
    """
    async with get_db_session() as session:
        result = await session.execute(select(KnowledgeDocument).where(KnowledgeDocument.is_active == True))
        docs = result.scalars().all()
        
        return {
            "total_documents": len(docs),
            "documents": [
                {
                    "id": d.id,
                    "entity_type": d.entity_type,
                    "category": d.category,
                    "title": d.title,
                    "content": d.content,
                    "tags": d.tags,
                    "metadata": d.metadata_json,
                    "content_hash": d.content_hash,
                    "created_at": d.created_at.isoformat() if d.created_at else None
                }
                for d in docs
            ]
        }

@router.post("/documents")
async def create_knowledge_document(payload: CreateDocumentRequest):
    """
    Dynamically insert a new document into PostgreSQL and enqueue non-blocking background embedding.
    """
    async with get_db_session() as session:
        # Check if exists
        result = await session.execute(select(KnowledgeDocument).where(KnowledgeDocument.id == payload.id))
        existing = result.scalar_one_or_none()
        
        canonical = CanonicalBuilder.build(payload.entity_type, {
            "title": payload.title,
            "category": payload.category,
            "content": payload.content,
            "tags": payload.tags,
            **payload.metadata
        })
        content_hash = ChangeDetector.compute_hash(canonical)

        if existing:
            existing.category = payload.category
            existing.title = payload.title
            existing.content = payload.content
            existing.canonical_text = canonical
            existing.tags = payload.tags
            existing.metadata_json = payload.metadata
            existing.content_hash = content_hash
            existing.is_active = True
            existing.updated_at = get_utc_now()
        else:
            doc = KnowledgeDocument(
                id=payload.id,
                entity_type=payload.entity_type,
                entity_id=payload.id,
                category=payload.category,
                title=payload.title,
                content=payload.content,
                canonical_text=canonical,
                tags=payload.tags,
                metadata_json=payload.metadata,
                content_hash=content_hash,
                is_active=True,
                created_at=get_utc_now()
            )
            session.add(doc)
        await session.commit()

    # Enqueue background job (Non-blocking)
    job_id = await EmbeddingQueue.enqueue(document_id=payload.id, action="INDEX")

    return {
        "status": "created",
        "document_id": payload.id,
        "job_id": job_id,
        "message": "Document stored in PostgreSQL. Embedding job enqueued in background."
    }

@router.delete("/documents/{document_id}")
async def delete_knowledge_document(document_id: str):
    """
    Deactivate and delete a knowledge document and its embeddings from PostgreSQL.
    """
    async with get_db_session() as session:
        result = await session.execute(select(KnowledgeDocument).where(KnowledgeDocument.id == document_id))
        doc = result.scalar_one_or_none()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc.is_active = False
        await session.delete(doc)
        await session.commit()

    return {"status": "deleted", "document_id": document_id}

# --- 5. Queue Status & Sync ---
@router.get("/queue/stats")
async def get_queue_statistics():
    """
    Inspect embedding background queue status.
    """
    stats = await EmbeddingQueue.get_queue_stats()
    return stats
