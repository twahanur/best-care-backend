"""
FastAPI Route Handlers for RAG Knowledge Search & AI Car Recommendation.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.rag_engine import RAGEngine
from app.services.vector_store import vector_store

router = APIRouter(prefix="/rag", tags=["RAG Knowledge & AI Matchmaker"])

class RAGQueryRequest(BaseModel):
    query: str = Field(..., examples=["What are the insurance options and security deposit rules?"])
    category: Optional[str] = Field(None, examples=["Rental Policy"])

class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[Dict[str, Any]]
    matched_vehicles: List[Dict[str, Any]]

class CarRecommendRequest(BaseModel):
    trip_description: str = Field(..., examples=["Family trip of 6 people going to Sylhet tea gardens with lots of luggage"])
    passengers: int = Field(default=4, ge=1, le=15, examples=[6])
    budget_per_day: Optional[float] = Field(None, examples=[150.0])
    terrain: Optional[str] = Field(None, examples=["Hills / Off-road"])

@router.post("/query", response_model=RAGQueryResponse)
async def handle_rag_query(payload: RAGQueryRequest):
    """
    Query the Car Rental RAG knowledge base for grounded answers on policies, fleet specs, and rules.
    """
    try:
        result = await RAGEngine.query(user_query=payload.query, category=payload.category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query execution failed: {str(e)}")

@router.post("/recommend-car")
async def handle_car_recommendation(payload: CarRecommendRequest):
    """
    AI Matchmaker: Intelligently recommends the best vehicle and alternatives based on trip characteristics.
    """
    try:
        result = await RAGEngine.recommend_vehicle(
            trip_description=payload.trip_description,
            passengers=payload.passengers,
            budget_per_day=payload.budget_per_day,
            terrain=payload.terrain
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Car recommendation failed: {str(e)}")

@router.get("/knowledge-docs")
async def get_knowledge_documents():
    """
    Inspect the raw knowledge base chunks currently indexed in the vector store.
    """
    if not vector_store.is_initialized:
        await vector_store.initialize()
    docs = vector_store.get_all_documents()
    return {
        "total_documents": len(docs),
        "documents": docs
    }
