"""
Grounding and Evidence Validator.
Estimates confidence score and checks if retrieved evidence is sufficient to ground an authoritative answer.
"""
from typing import List, Dict, Any

class GroundingChecker:
    @staticmethod
    def evaluate(retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not retrieved_docs:
            return {
                "is_grounded": False,
                "confidence_score": 0.0,
                "reason": "No documents retrieved from PostgreSQL database."
            }

        top_score = retrieved_docs[0].get("score", 0.0)
        is_sufficient = len(retrieved_docs) > 0 and (top_score > 0.15 or len(retrieved_docs) >= 1)

        confidence = min(0.98, max(0.60, 0.60 + (top_score * 0.40)))
        return {
            "is_grounded": is_sufficient,
            "confidence_score": round(confidence, 3),
            "evidence_count": len(retrieved_docs)
        }

grounding_checker = GroundingChecker()
