"""
Entity and Constraint Extractor for Car Rental Inquiries.
Extracts passengers/seats, rental duration, budget, category, destination, and terrain requirements.
"""
import re
from typing import Dict, Any, Optional

class EntityExtractor:
    @staticmethod
    def extract(text: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "seats": None,
            "duration_days": None,
            "budget_max": None,
            "category": None,
            "destination": None,
            "terrain": None
        }
        
        lower = text.lower()

        # 1. Passengers / Seats count (e.g., "6 jon", "7 people", "family of 5", "6 seater")
        seat_match = re.search(r"(\d+)\s*(?:people|persons?|passengers?|jon|seater|members?)", lower)
        if seat_match:
            result["seats"] = int(seat_match.group(1))
        else:
            seat_word_match = re.search(r"family of\s*(\d+)", lower)
            if seat_word_match:
                result["seats"] = int(seat_word_match.group(1))

        # 2. Duration / Days (e.g., "4 days", "4 din", "3 diner", "5 day")
        day_match = re.search(r"(\d+)\s*(?:days?|dins?|diner|nights?)", lower)
        if day_match:
            result["duration_days"] = int(day_match.group(1))

        # 3. Budget (e.g., "$150", "150$", "5000 taka", "5000 tk", "150 usd")
        budget_match = re.search(r"(?:\$|usd\s*|tk\s*|taka\s*)?(\d{2,6})\s*(?:\$|usd|taka|tk|bdt)?", lower)
        if budget_match:
            val = float(budget_match.group(1))
            if val > 30:  # Reasonable budget amount
                result["budget_max"] = val

        # 4. Vehicle Category
        if re.search(r"\bsuv\b|4x4|4wd", lower):
            result["category"] = "SUV"
        elif re.search(r"\bsedan\b|car", lower) and "suv" not in lower and "van" not in lower:
            result["category"] = "Sedan"
        elif re.search(r"\bvan\b|hiace|microbus|micro", lower):
            result["category"] = "Van"
        elif re.search(r"\bluxury\b|mercedes|vip", lower):
            result["category"] = "Luxury"
        elif re.search(r"\belectric\b|\bev\b|tesla", lower):
            result["category"] = "Electric"
        elif re.search(r"\bsports\b|mustang|convertible", lower):
            result["category"] = "Sports"

        # 5. Destination & Terrain
        if "sajek" in lower:
            result["destination"] = "Sajek Valley"
            result["terrain"] = "Mountainous & Hilly Off-Road"
        elif "sylhet" in lower:
            result["destination"] = "Sylhet"
            result["terrain"] = "Tea Gardens & Hilly Highways"
        elif "bandarban" in lower:
            result["destination"] = "Bandarban"
            result["terrain"] = "Steep Mountain Roads & Off-Road"
        elif re.search(r"mountain|hills?|off-?road|pahar", lower):
            result["terrain"] = "Mountain / Off-Road"
        elif re.search(r"highway|inter-?district", lower):
            result["terrain"] = "Paved Highway"
        elif re.search(r"city|urban|commute", lower):
            result["terrain"] = "City Streets"

        return result

entity_extractor = EntityExtractor()
