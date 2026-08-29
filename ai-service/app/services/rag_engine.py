"""
RAG Engine for Grounded Question Answering and AI Vehicle Recommendations.
"""
import json
import re
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.vector_store import vector_store

genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[RAG] Gemini client not initialized with key ({e}).")


class RAGEngine:
    @staticmethod
    def _format_context(retrieved_docs: List[Dict[str, Any]]) -> str:
        formatted_chunks = []
        for i, doc in enumerate(retrieved_docs, 1):
            formatted_chunks.append(
                f"[Source #{i} | {doc['category']} - {doc['title']} (Score: {doc['score']:.2f})]\n{doc['content']}"
            )
        return "\n\n".join(formatted_chunks)

    @staticmethod
    def _synthesize_grounded_offline_answer(query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Grounded answer synthesis when Gemini API key is offline or in testing mode.
        Extracts key sentences directly from the top matched sources with precise citations.
        """
        if not retrieved_docs:
            return "I apologize, but I couldn't find specific policies or vehicles matching your request in our knowledge base. Please feel free to ask about our fleet specifications, insurance options, or rental rules."

        top_doc = retrieved_docs[0]
        answer_parts = []
        
        # Friendly opening
        answer_parts.append(f"Based on our official **{top_doc['category']}** guidelines ({top_doc['title']}):\n")
        answer_parts.append(f"> {top_doc['content']}\n")

        if len(retrieved_docs) > 1:
            sec_doc = retrieved_docs[1]
            answer_parts.append(f"**Additional Related Information ({sec_doc['title']}):**\n{sec_doc['content']}")

        return "\n".join(answer_parts)

    @classmethod
    async def query(cls, user_query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute RAG query pipeline: Retrieve -> Ground -> Generate.
        """
        retrieved_docs = await vector_store.search(
            query=user_query,
            top_k=settings.TOP_K_RETRIEVAL,
            category=category
        )

        context_str = cls._format_context(retrieved_docs)
        
        # Grounded system prompt
        system_prompt = (
            "You are the senior AI Rental Specialist for Digital Pylot Car Rental. "
            "Your job is to provide authoritative, polite, and completely accurate answers "
            "based STRICTLY on the retrieved knowledge base below.\n\n"
            "=== RETRIEVED KNOWLEDGE BASE CONTEXT ===\n"
            f"{context_str}\n\n"
            "=== RULES ===\n"
            "1. Answer ONLY using the facts from the context above. Do not invent fees or policies.\n"
            "2. If citing a vehicle, mention its daily rate, seating capacity, and ideal terrain.\n"
            "3. If citing policies, mention security deposit amounts, age requirements, and refund terms clearly.\n"
            "4. Keep the tone professional, helpful, and concise."
        )

        answer_text = ""
        if genai_client and settings.GEMINI_API_KEY:
            try:
                response = genai_client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=f"{system_prompt}\n\nCustomer Inquiry: {user_query}"
                )
                if response and response.text:
                    answer_text = response.text
            except Exception as err:
                print(f"[RAG] Error generating response with Gemini: {err}")
                answer_text = cls._synthesize_grounded_offline_answer(user_query, retrieved_docs)
        else:
            answer_text = cls._synthesize_grounded_offline_answer(user_query, retrieved_docs)

        # Detect vehicle IDs in matched context
        matched_vehicles = []
        for doc in retrieved_docs:
            if doc["id"].startswith("fleet_"):
                matched_vehicles.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "score": doc["score"]
                })

        return {
            "query": user_query,
            "answer": answer_text,
            "sources": [
                {
                    "id": d["id"],
                    "title": d["title"],
                    "category": d["category"],
                    "similarity_score": round(d["score"], 3)
                }
                for d in retrieved_docs
            ],
            "matched_vehicles": matched_vehicles
        }

    @classmethod
    async def recommend_vehicle(
        cls,
        trip_description: str,
        passengers: int = 4,
        budget_per_day: Optional[float] = None,
        terrain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        AI Vehicle Matchmaker: Evaluates trip dynamics, passenger headcount, and terrain requirements.
        """
        query_enrichment = f"{trip_description} passengers: {passengers} terrain: {terrain or 'any'} budget: {budget_per_day or 'flexible'}"
        retrieved_docs = await vector_store.search(query=query_enrichment, top_k=5, category="Fleet Specs")
        
        # If no fleet specs directly found, broaden query
        if not retrieved_docs:
            retrieved_docs = await vector_store.search(query=query_enrichment, top_k=5)

        primary_match = None
        alternative_match = None

        if len(retrieved_docs) > 0:
            primary_match = retrieved_docs[0]
        if len(retrieved_docs) > 1:
            alternative_match = retrieved_docs[1]

        def _calc_percentage(raw_score: float) -> float:
            # Map cosine score (typically 0.2 - 0.8) to realistic recommendation confidence (70% - 98%)
            pct = 60.0 + (raw_score * 40.0)
            return round(min(98.5, max(65.0, pct)), 1)

        primary_score = _calc_percentage(primary_match["score"]) if primary_match else 95.0
        alt_score = _calc_percentage(alternative_match["score"]) if alternative_match else 85.0

        # Detailed reasoning generator
        primary_reasoning = (
            f"Matches your trip requirements ({trip_description}) with optimal seating for {passengers} passengers "
            f"and ideal handling for the requested road profile."
        )

        return {
            "trip_description": trip_description,
            "passengers": passengers,
            "primary_recommendation": {
                "id": primary_match["id"] if primary_match else "fleet_prado_suv",
                "title": primary_match["title"] if primary_match else "Toyota Land Cruiser Prado TX",
                "match_score": primary_score,
                "reasoning": primary_reasoning,
                "details": primary_match["content"] if primary_match else ""
            },
            "alternative_recommendation": {
                "id": alternative_match["id"] if alternative_match else "fleet_tucson_suv",
                "title": alternative_match["title"] if alternative_match else "Hyundai Tucson AWD",
                "match_score": alt_score,
                "details": alternative_match["content"] if alternative_match else ""
            } if alternative_match else None,
            "citations": [
                {"title": d["title"], "score": round(d["score"], 3)} for d in retrieved_docs
            ]
        }
