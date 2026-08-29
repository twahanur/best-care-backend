"""
Agentic RAG Orchestration Engine.
Orchestrates multi-turn conversation memory, intent extraction, hybrid retrieval,
reranking, evidence grounding, and multilingual response generation.
"""
import re
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.query.language_detector import language_detector
from app.query.normalizer import query_normalizer
from app.query.intent_detector import intent_detector
from app.query.entity_extractor import entity_extractor
from app.retrieval.hybrid_retriever import hybrid_retriever
from app.ranking.reranker import reranker
from app.ranking.relevance_filter import relevance_filter
from app.context.context_builder import context_builder
from app.context.grounding_checker import grounding_checker
from app.memory.conversation_memory import conversation_memory
from app.memory.user_memory import user_memory
from app.agent.prompt_templates import SYSTEM_RAG_AGENT_PROMPT, OFFLINE_SYNTHESIS_TEMPLATE

# Initialize Gemini Client if API key is present
genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[RAGAgent] Gemini client not initialized with key ({e}). Using resilient multilingual fallback.")


class RAGAgent:
    @classmethod
    def _synthesize_grounded_offline_answer(
        cls,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        language: str,
        history: List[Dict[str, Any]]
    ) -> str:
        """
        Multilingual grounded answer synthesis when Gemini API key is offline or in test mode.
        """
        if not retrieved_docs:
            if language == "bangla":
                return "দুঃখিত, আমাদের ডাটাবেজে আপনার অনুসন্ধানের সাথে মিলে এমন সুনির্দিষ্ট তথ্য পাওয়া যায়নি। অনুগ্রহ করে আমাদের ফ্লিট বা ভাড়ার নিয়মাবলী সম্পর্কে বিস্তারিত জিজ্ঞাসা করুন।"
            elif language == "banglish":
                return "Dukkhoito, amader database e apnar query onujayi kono specific vehicle ba policy pawa jayni. Apni fleet specs ba security deposit niye jante chaile bolte paren."
            else:
                return "I apologize, but I couldn't find specific policies or vehicles matching your request in our database. Please feel free to ask about our fleet specifications, insurance options, or rental rules."

        top_doc = retrieved_docs[0]
        extra_info = ""
        if len(retrieved_docs) > 1:
            sec_doc = retrieved_docs[1]
            if language == "bangla":
                extra_info = f"\n\n**অতিরিক্ত প্রাসঙ্গিক তথ্য ({sec_doc['title']}):**\n{sec_doc['content']}"
            elif language == "banglish":
                extra_info = f"\n\n**Additional Related Info ({sec_doc['title']}):**\n{sec_doc['content']}"
            else:
                extra_info = f"\n\n**Additional Related Information ({sec_doc['title']}):**\n{sec_doc['content']}"

        tmpl = OFFLINE_SYNTHESIS_TEMPLATE.get(language, OFFLINE_SYNTHESIS_TEMPLATE["english"])
        return tmpl.format(
            category=top_doc.get("category", "Guide"),
            title=top_doc.get("title", ""),
            content=top_doc.get("content", ""),
            extra_info=extra_info
        )

    @classmethod
    async def chat(
        cls,
        user_query: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes complete Agentic RAG pipeline:
        1. Conversation Session Management & History Retrieval
        2. Language, Intent & Entity Extraction
        3. Conversational Query Expansion
        4. PostgreSQL Pre-Computed Vector & Hybrid Retrieval
        5. Reranking & Context Construction
        6. Grounded Multilingual Synthesis (Gemini / Resilient Fallback)
        7. History Persistence
        """
        # 1. Manage Conversation Session
        active_session_id = await conversation_memory.get_or_create_conversation(session_id, user_id)
        history = await conversation_memory.get_history(active_session_id)

        # 2. Query Analysis
        lang = language_detector.detect(user_query)
        intent = intent_detector.detect(user_query)
        entities = entity_extractor.extract(user_query)

        # 3. Conversational Query Expansion (incorporate past turns if follow-up)
        retrieval_query = user_query
        if history and len(history) >= 2:
            last_assistant_msg = history[-1]["content"] if history[-1]["role"] == "assistant" else ""
            # If current query is brief or referencing previous turn
            if len(user_query.split()) <= 6 or any(k in user_query.lower() for k in ["that", "it", "this", "eta", "otar", "cost", "total", "price", "deposit"]):
                retrieval_query = f"{user_query} Context: {last_assistant_msg[:200]}"

        expanded_query = query_normalizer.expand_for_retrieval(retrieval_query)

        # 4. Hybrid Retrieval over PostgreSQL Database
        raw_candidates = await hybrid_retriever.retrieve(
            query=expanded_query,
            category=category,
            constraints=entities,
            top_k=settings.MAX_CANDIDATES
        )

        # 5. Reranking & Relevance Filtering
        reranked_docs = reranker.rerank(raw_candidates, user_query, intent, entities)
        final_docs = relevance_filter.filter(reranked_docs, top_k=settings.FINAL_TOP_K)

        # 6. Context & Grounding Check
        context_str = context_builder.build(final_docs)
        grounding_result = grounding_checker.evaluate(final_docs)

        # Format history for LLM
        history_lines = []
        for msg in history[-6:]:  # Last 3 turns
            role_label = "Customer" if msg["role"] == "user" else "AI Specialist"
            history_lines.append(f"{role_label}: {msg['content']}")
        history_str = "\n".join(history_lines) if history_lines else "No previous conversation history."

        # Fetch user preferences
        user_prefs = await user_memory.get_user_preferences(user_id) if user_id else {}
        user_memory_str = "\n".join([f"- {k}: {v}" for k, v in user_prefs.items()]) if user_prefs else "No saved user preferences."

        # 7. LLM Grounded Generation
        answer_text = ""
        system_prompt = SYSTEM_RAG_AGENT_PROMPT.format(
            context_str=context_str,
            history_str=history_str,
            user_memory_str=user_memory_str
        )

        if genai_client and settings.GEMINI_API_KEY:
            try:
                response = genai_client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=f"{system_prompt}\n\nCustomer Inquiry: {user_query}"
                )
                if response and response.text:
                    answer_text = response.text
            except Exception as err:
                print(f"[RAGAgent] Gemini generation error: {err}. Using multilingual grounded fallback.")
                answer_text = cls._synthesize_grounded_offline_answer(user_query, final_docs, lang, history)
        else:
            answer_text = cls._synthesize_grounded_offline_answer(user_query, final_docs, lang, history)

        # Extract matched vehicle IDs
        matched_vehicles = []
        for doc in final_docs:
            if doc.get("id", "").startswith("fleet_") or doc.get("category") == "Fleet Specs":
                matched_vehicles.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "score": round(doc.get("similarity_score", doc.get("score", 0.9)), 3)
                })

        formatted_sources = [
            {
                "id": d["id"],
                "title": d["title"],
                "category": d["category"],
                "similarity_score": round(d.get("similarity_score", d.get("score", 0.0)), 3),
                "rrf_score": round(d.get("rrf_score", 0.0), 4)
            }
            for d in final_docs
        ]

        # 8. Save Conversation Turns to PostgreSQL
        await conversation_memory.add_message(
            session_id=active_session_id,
            role="user",
            content=user_query,
            language=lang,
            intent=intent
        )
        await conversation_memory.add_message(
            session_id=active_session_id,
            role="assistant",
            content=answer_text,
            language=lang,
            intent=intent,
            sources=formatted_sources,
            matched_vehicles=matched_vehicles
        )

        return {
            "session_id": active_session_id,
            "query": user_query,
            "answer": answer_text,
            "language": lang,
            "intent": intent,
            "sources": formatted_sources,
            "matched_vehicles": matched_vehicles,
            "confidence_score": grounding_result["confidence_score"]
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
        constraints = {"seats": passengers, "budget_max": budget_per_day, "terrain": terrain}

        candidates = await hybrid_retriever.retrieve(
            query=query_enrichment,
            category="Fleet Specs",
            constraints=constraints,
            top_k=5
        )
        
        if not candidates:
            candidates = await hybrid_retriever.retrieve(query=query_enrichment, top_k=5)

        primary_match = candidates[0] if candidates else None
        alternative_match = candidates[1] if len(candidates) > 1 else None

        def _calc_percentage(raw_score: float) -> float:
            pct = 60.0 + (raw_score * 40.0)
            return round(min(98.5, max(65.0, pct)), 1)

        primary_score = _calc_percentage(primary_match.get("similarity_score", 0.9)) if primary_match else 95.0
        alt_score = _calc_percentage(alternative_match.get("similarity_score", 0.75)) if alternative_match else 85.0

        primary_reasoning = (
            f"Optimal choice for {passengers} passengers on your journey ({trip_description}) "
            f"with ideal ground clearance and handling for {terrain or 'highway and hills'}."
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
                {
                    "title": d["title"],
                    "score": round(d.get("similarity_score", d.get("score", 0.9)), 3)
                }
                for d in candidates
            ]
        }

rag_agent = RAGAgent()
