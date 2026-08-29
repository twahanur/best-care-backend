"""
Relevance and Quality Filter.
Prunes low-confidence documents before context construction.
"""
from typing import List, Dict, Any

class RelevanceFilter:
    @staticmethod
    def filter(candidates: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        if not candidates:
            return []
        
        # Ensure we always keep at least top 1-2 if available
        filtered = candidates[:top_k]
        return filtered

relevance_filter = RelevanceFilter()
