"""
Metadata Constraint Filter.
Filters candidate documents based on extracted query constraints.
"""
from typing import List, Dict, Any

class MetadataFilter:
    @staticmethod
    def apply(candidates: List[Dict[str, Any]], constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not constraints:
            return candidates

        filtered = []
        for doc in candidates:
            meta = doc.get("metadata", {}) or {}
            
            # 1. Seats constraint
            required_seats = constraints.get("seats")
            if required_seats and "seats" in meta:
                if meta["seats"] < required_seats:
                    continue

            # 2. Budget constraint (daily rate)
            max_budget = constraints.get("budget_max")
            if max_budget and "dailyRate" in meta:
                if meta["dailyRate"] > max_budget:
                    continue

            # 3. Category constraint
            cat = constraints.get("category")
            if cat and doc.get("category") == "Fleet Specs":
                doc_cat = meta.get("category", "")
                if cat.lower() not in doc_cat.lower() and cat.lower() not in doc.get("title", "").lower():
                    # Soft filter: Keep if high similarity or continue
                    pass

            filtered.append(doc)

        return filtered if filtered else candidates

metadata_filter = MetadataFilter()
