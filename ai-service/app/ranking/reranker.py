"""
Cross-Score Reranker.
Reranks candidate retrieved documents considering intent alignment, entity hits, and semantic density.
"""
from typing import List, Dict, Any

class Reranker:
    @staticmethod
    def rerank(
        candidates: List[Dict[str, Any]],
        query: str,
        intent: str,
        entities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        reranked = []
        q_lower = query.lower()

        for doc in candidates:
            base_score = doc.get("rrf_score", 0.0) * 100.0 + doc.get("similarity_score", 0.0) * 10.0
            bonus = 0.0

            cat = doc.get("category", "")
            title = doc.get("title", "").lower()
            content = doc.get("content", "").lower()

            # Intent alignment bonuses
            if intent == "POLICY_INQUIRY" and "policy" in cat.lower():
                bonus += 5.0
            elif intent == "INSURANCE_INQUIRY" and "insurance" in cat.lower():
                bonus += 5.0
            elif intent == "TRIP_RECOMMENDATION" and ("trip" in cat.lower() or "fleet" in cat.lower()):
                bonus += 5.0
            elif intent == "VEHICLE_SEARCH" and "fleet" in cat.lower():
                bonus += 5.0

            # Exact title or vehicle token match
            for word in q_lower.split():
                if len(word) > 3 and word in title:
                    bonus += 3.0

            final_score = base_score + bonus
            doc_copy = dict(doc)
            doc_copy["rerank_score"] = round(final_score, 4)
            reranked.append(doc_copy)

        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        return reranked

reranker = Reranker()
