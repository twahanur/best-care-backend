import re
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List

# Standard location aliases in Bangladesh
LOCATION_KEYWORDS = {
    "dhaka": "Dhaka",
    "gulshan": "Gulshan",
    "banani": "Banani",
    "uttara": "Uttara",
    "dhanmondi": "Dhanmondi",
    "airport": "Hazrat Shahjalal Intl Airport (DAC)",
    "dac": "Hazrat Shahjalal Intl Airport (DAC)",
    "khulna": "Khulna",
    "khulne": "Khulna",
    "sonadanga": "Sonadanga, Khulna",
    "chittagong": "Chittagong",
    "chattogram": "Chittagong",
    "agrabad": "Agrabad, Chittagong",
    "sylhet": "Sylhet",
    "jaflong": "Jaflong, Sylhet",
    "sreemangal": "Sreemangal",
    "cox's bazar": "Cox's Bazar",
    "coxsbazar": "Cox's Bazar",
    "sajek": "Sajek Valley",
    "bandarban": "Bandarban",
    "rajshahi": "Rajshahi"
}

# Car Model and Category mappings
VEHICLE_PATTERNS = {
    "prado": {"id": "car_prado_suv", "name": "Toyota Land Cruiser Prado TX", "category": "SUV", "dailyRate": 145, "seats": 7},
    "tucson": {"id": "car_tucson_suv", "name": "Hyundai Tucson AWD", "category": "SUV", "dailyRate": 85, "seats": 5},
    "tesla": {"id": "car_tesla_modely", "name": "Tesla Model Y Long Range", "category": "Electric", "dailyRate": 110, "seats": 5},
    "mercedes": {"id": "car_mercedes_eclass", "name": "Mercedes-Benz E-Class AMG Line", "category": "Luxury", "dailyRate": 160, "seats": 5},
    "camry": {"id": "car_camry_hybrid", "name": "Toyota Camry Premium Hybrid", "category": "Sedan", "dailyRate": 70, "seats": 5},
    "hiace": {"id": "car_hiace_luxury", "name": "Toyota HiAce Grandia Luxury", "category": "Van", "dailyRate": 130, "seats": 11},
    "civic": {"id": "car_civic_sport", "name": "Honda Civic Sport", "category": "Sedan", "dailyRate": 55, "seats": 5},
    "mustang": {"id": "car_mustang_gt", "name": "Ford Mustang GT Convertible", "category": "Sports", "dailyRate": 175, "seats": 4},
    "audi": {"id": "car_audi_a6", "name": "Audi A6 Business Executive", "category": "Luxury", "dailyRate": 95, "seats": 5},
    "jaguar": {"id": "car_jaguar_xe", "name": "Jaguar XE L Prestige", "category": "Luxury", "dailyRate": 85, "seats": 5}
}

CATEGORY_KEYWORDS = {
    "suv": "SUV",
    "sedan": "Sedan",
    "van": "Van",
    "micro": "Van",
    "electric": "Electric",
    "ev": "Electric",
    "luxury": "Luxury",
    "sports": "Sports",
    "convertible": "Sports",
    "4x4": "SUV",
    "4wd": "SUV"
}

class EntityExtractor:
    @staticmethod
    def extract(text: str, current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Extracts structured entities from multi-lingual user query.
        """
        now = current_time or datetime.now(timezone.utc)
        text_lower = text.lower()
        entities: Dict[str, Any] = {
            "locations": [],
            "pickup_location": None,
            "dropoff_location": None,
            "pickup_date": None,
            "dropoff_date": None,
            "pickup_time": None,
            "seats": None,
            "vehicle_name": None,
            "vehicle_id": None,
            "category": None,
            "budget_max": None,
            "duration_days": None,
            "is_confirmation": False,
            "is_cancellation": False
        }

        # 1. Extract Locations
        found_locs = []
        for loc_key, loc_name in LOCATION_KEYWORDS.items():
            if re.search(rf"\b{loc_key}\b", text_lower):
                if loc_name not in found_locs:
                    found_locs.append(loc_name)

        entities["locations"] = found_locs

        # Determine pickup vs dropoff if patterns like "Khulna theke Dhaka" or "from Khulna to Dhaka"
        theke_match = re.search(r"(\w+)\s+(?:theke|from)\s+(\w+)\s+(?:te|to)?", text_lower)
        if theke_match:
            p_cand, d_cand = theke_match.group(1), theke_match.group(2)
            for k, v in LOCATION_KEYWORDS.items():
                if k in p_cand and not entities["pickup_location"]:
                    entities["pickup_location"] = v
                if k in d_cand and not entities["dropoff_location"]:
                    entities["dropoff_location"] = v

        if not entities["pickup_location"] and found_locs:
            entities["pickup_location"] = found_locs[0]
            if len(found_locs) > 1 and not entities["dropoff_location"]:
                entities["dropoff_location"] = found_locs[1]

        # Specific pickup point override (e.g. "sonadanga theke")
        if "sonadanga" in text_lower:
            entities["pickup_location"] = "Sonadanga, Khulna"

        # 2. Extract Dates (Bangla, Banglish, Relative, and Specific)
        if re.search(r"\b(agamikal|kalke|kal|tomorrow)\b", text_lower):
            target_date = now + timedelta(days=1)
            entities["pickup_date"] = target_date.strftime("%Y-%m-%d")
        elif re.search(r"\b(poroshu|day after tomorrow)\b", text_lower):
            target_date = now + timedelta(days=2)
            entities["pickup_date"] = target_date.strftime("%Y-%m-%d")
        elif re.search(r"\b(aaj|ajke|today)\b", text_lower):
            entities["pickup_date"] = now.strftime("%Y-%m-%d")

        tarik_match = re.search(r"\b(\d{1,2})\s*(?:tarik|tarikh|th|st|nd|rd)\b", text_lower)
        if tarik_match:
            day = int(tarik_match.group(1))
            month = now.month
            year = now.year
            if day < now.day:
                month = month + 1
                if month > 12:
                    month = 1
                    year += 1
            try:
                dt = datetime(year, month, day)
                entities["pickup_date"] = dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

        iso_match = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", text_lower)
        if iso_match:
            entities["pickup_date"] = iso_match.group(0)

        # 3. Extract Time (strict to prevent false matches on non-time digits)
        time_match = re.search(r"\b(?:sokal|dupur|bikal|shondha|raat)\s*(\d{1,2})(?::(\d{2}))?\s*(?:tay|ta|am|pm)?\b|\b(\d{1,2})(?::(\d{2}))?\s*(?:am|pm|tay|ta)\b", text_lower)
        if time_match:
            match_str = time_match.group(0)
            digits = re.findall(r"\d+", match_str)
            if digits:
                hour = int(digits[0])
                min_str = digits[1] if len(digits) > 1 else "00"
                if any(w in match_str for w in ["shondha", "raat", "bikal", "pm"]) and hour < 12:
                    hour += 12
                elif any(w in match_str for w in ["sokal", "am"]) and hour == 12:
                    hour = 0
                entities["pickup_time"] = f"{hour:02d}:{min_str}"

        # 4. Extract Vehicle Models & Categories
        for v_key, v_info in VEHICLE_PATTERNS.items():
            if re.search(rf"\b{v_key}\b", text_lower):
                entities["vehicle_name"] = v_info["name"]
                entities["vehicle_id"] = v_info["id"]
                entities["category"] = v_info["category"]
                break

        if not entities["category"]:
            for cat_key, cat_val in CATEGORY_KEYWORDS.items():
                if re.search(rf"\b{cat_key}\b", text_lower):
                    entities["category"] = cat_val
                    break

        # 5. Extract Seats: "7 seat", "7-seater", "6 jon", "6 passenger", "6 joner"
        seat_match = re.search(r"(\d+)\s*(?:seat|seater|jon|joner|passenger|person)", text_lower)
        if seat_match:
            entities["seats"] = int(seat_match.group(1))

        # 6. Extract Duration: "3 din", "3 days", "3 diner"
        day_match = re.search(r"(\d+)\s*(?:din|diner|day|days)", text_lower)
        if day_match:
            entities["duration_days"] = int(day_match.group(1))

        # 7. Extract Confirmations / Cancellations
        if re.search(r"\b(haan|yes|confirm|thik ache|proceed|sure|koro|korbo|book it|done|cholo)\b", text_lower):
            # Only treat as confirmation if not a cancellation or general instruction
            if not re.search(r"\b(na|cancel)\b", text_lower):
                entities["is_confirmation"] = True
        if re.search(r"\b(na|cancel|no|stop|dorkar nai|bad dao|lagbe na)\b", text_lower):
            entities["is_cancellation"] = True

        return entities

entity_extractor = EntityExtractor()
