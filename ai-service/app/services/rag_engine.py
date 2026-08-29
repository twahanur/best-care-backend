"""
RAG Engine Compatibility Layer.
Routes legacy RAGEngine calls to the new production-grade Agentic RAG Agent.
"""
from typing import List, Dict, Any, Optional
from app.agent.rag_agent import rag_agent

class RAGEngine:
    @classmethod
    async def query(cls, user_query: str, category: Optional[str] = None) -> Dict[str, Any]:
        res = await rag_agent.chat(user_query=user_query, category=category)
        return {
            "query": res["query"],
            "answer": res["answer"],
            "sources": res["sources"],
            "matched_vehicles": res["matched_vehicles"]
        }

    @classmethod
    async def recommend_vehicle(
        cls,
        trip_description: str,
        passengers: int = 4,
        budget_per_day: Optional[float] = None,
        terrain: Optional[str] = None
    ) -> Dict[str, Any]:
        return await rag_agent.recommend_vehicle(
            trip_description=trip_description,
            passengers=passengers,
            budget_per_day=budget_per_day,
            terrain=terrain
        )
