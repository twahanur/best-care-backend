import re
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List

# Bangla digit mapping
BANGLA_DIGITS = {
    "০": "0", "১": "1", "২": "2", "৩": "3", "৪": "4",
    "৫": "5", "৬": "6", "৭": "7", "৮": "8", "৯": "9"
}

WORD_NUMBERS = {
    "ek": 1, "one": 1, "এক": 1,
    "dui": 2, "two": 2, "দুই": 2,
    "tin": 3, "three": 3, "তিন": 3,
    "char": 4, "four": 4, "চার": 4,
    "pach": 5, "paach": 5, "five": 5, "পাঁচ": 5,
    "choy": 6, "six": 6, "ছয়": 6,
    "sat": 7, "shaat": 7, "seven": 7, "সাত": 7,
    "at": 8, "aath": 8, "eight": 8, "আট": 8,
    "noy": 9, "nine": 9, "নয়": 9,
    "dosh": 10, "ten": 10, "দশ": 10
}

# Standard location aliases in Bangladesh
LOCATION_KEYWORDS = {
    "dhaka": "Dhaka",
    "ঢাকা": "Dhaka",
    "gulshan": "Gulshan",
    "গুলশান": "Gulshan",
    "banani": "Banani",
    "বনানী": "Banani",
    "uttara": "Uttara",
    "উত্তরা": "Uttara",
    "dhanmondi": "Dhanmondi",
    "ধানমন্ডি": "Dhanmondi",
    "airport": "Hazrat Shahjalal Intl Airport (DAC)",
    "এয়ারপোর্ট": "Hazrat Shahjalal Intl Airport (DAC)",
    "বিমানবন্দর": "Hazrat Shahjalal Intl Airport (DAC)",
    "dac": "Hazrat Shahjalal Intl Airport (DAC)",
    "khulna": "Khulna",
    "খুলনা": "Khulna",
    "khulne": "Khulna",
    "sonadanga": "Sonadanga, Khulna",
    "সোনাডাঙ্গা": "Sonadanga, Khulna",
    "chittagong": "Chittagong",
    "চট্টগ্রাম": "Chittagong",
    "chattogram": "Chittagong",
    "agrabad": "Agrabad, Chittagong",
    "আগ্রাবাদ": "Agrabad, Chittagong",
    "sylhet": "Sylhet",
    "সিলেট": "Sylhet",
    "jaflong": "Jaflong, Sylhet",
    "জাফলং": "Jaflong, Sylhet",
    "sreemangal": "Sreemangal",
    "শ্রীমঙ্গল": "Sreemangal",
    "cox's bazar": "Cox's Bazar",
    "coxsbazar": "Cox's Bazar",
    "কক্সবাজার": "Cox's Bazar",
    "sajek": "Sajek Valley",
    "সাজেক": "Sajek Valley",
    "bandarban": "Bandarban",
    "বান্দরবান": "Bandarban",
    "rajshahi": "Rajshahi",
    "রাজশাহী": "Rajshahi"
}

# Car Model and Category mappings
VEHICLE_PATTERNS = {
    "q7": {"id": "car_audi_q7", "name": "Audi Q7 55 TFSI Quattro", "category": "SUV", "dailyRate": 180, "seats": 7},
    "crv": {"id": "car_honda_crv", "name": "Honda CR-V Turbo Prestige", "category": "SUV", "dailyRate": 80, "seats": 7},
    "cr-v": {"id": "car_honda_crv", "name": "Honda CR-V Turbo Prestige", "category": "SUV", "dailyRate": 80, "seats": 7},
    "prado": {"id": "car_prado_suv", "name": "Toyota Land Cruiser Prado TX", "category": "SUV", "dailyRate": 145, "seats": 7},
    "land cruiser": {"id": "car_prado_suv", "name": "Toyota Land Cruiser Prado TX", "category": "SUV", "dailyRate": 145, "seats": 7},
    "tucson": {"id": "car_tucson_suv", "name": "Hyundai Tucson Limited Edition", "category": "SUV", "dailyRate": 75, "seats": 5},
    "modely": {"id": "car_tesla_modely", "name": "Tesla Model Y Long Range", "category": "Electric", "dailyRate": 110, "seats": 5},
    "model y": {"id": "car_tesla_modely", "name": "Tesla Model Y Long Range", "category": "Electric", "dailyRate": 110, "seats": 5},
    "tesla": {"id": "car_tesla_modely", "name": "Tesla Model Y Long Range", "category": "Electric", "dailyRate": 110, "seats": 5},
    "mercedes": {"id": "car_mercedes_eclass", "name": "Mercedes-Benz E-Class AMG Line", "category": "Luxury", "dailyRate": 160, "seats": 5},
    "eclass": {"id": "car_mercedes_eclass", "name": "Mercedes-Benz E-Class AMG Line", "category": "Luxury", "dailyRate": 160, "seats": 5},
    "e-class": {"id": "car_mercedes_eclass", "name": "Mercedes-Benz E-Class AMG Line", "category": "Luxury", "dailyRate": 160, "seats": 5},
    "benz": {"id": "car_mercedes_eclass", "name": "Mercedes-Benz E-Class AMG Line", "category": "Luxury", "dailyRate": 160, "seats": 5},
    "bmw": {"id": "car_bmw_530i", "name": "BMW 530i M Sport", "category": "Luxury", "dailyRate": 140, "seats": 5},
    "530i": {"id": "car_bmw_530i", "name": "BMW 530i M Sport", "category": "Luxury", "dailyRate": 140, "seats": 5},
    "camry": {"id": "car_camry_hybrid", "name": "Toyota Camry Premium Hybrid", "category": "Sedan", "dailyRate": 70, "seats": 5},
    "hiace": {"id": "car_hiace_luxury", "name": "Toyota HiAce Grandia Luxury", "category": "Van", "dailyRate": 130, "seats": 11},
    "grandia": {"id": "car_hiace_luxury", "name": "Toyota HiAce Grandia Luxury", "category": "Van", "dailyRate": 130, "seats": 11},
    "civic": {"id": "car_civic_sport", "name": "Honda Civic Sport", "category": "Sedan", "dailyRate": 55, "seats": 5},
    "mustang": {"id": "car_mustang_gt", "name": "Ford Mustang GT Convertible", "category": "Sports", "dailyRate": 175, "seats": 4},
    "audi": {"id": "car_audi_a6", "name": "Audi A6 Business Executive", "category": "Luxury", "dailyRate": 95, "seats": 5},
    "a6": {"id": "car_audi_a6", "name": "Audi A6 Business Executive", "category": "Luxury", "dailyRate": 95, "seats": 5},
    "jaguar": {"id": "car_jaguar_xe", "name": "Jaguar XE L Prestige", "category": "Luxury", "dailyRate": 85, "seats": 5},
    "xe": {"id": "car_jaguar_xe", "name": "Jaguar XE L Prestige", "category": "Luxury", "dailyRate": 85, "seats": 5}
}

CATEGORY_KEYWORDS = {
    "suv": "SUV",
    "এসইউভি": "SUV",
    "sedan": "Sedan",
    "সেডান": "Sedan",
    "van": "Van",
    "ভ্যান": "Van",
    "micro": "Van",
    "মাইক্রো": "Van",
    "electric": "Electric",
    "ইলেকট্রিক": "Electric",
    "ev": "Electric",
    "luxury": "Luxury",
    "লাক্সারি": "Luxury",
    "sports": "Sports",
    "স্পোর্টস": "Sports",
    "convertible": "Sports",
    "4x4": "SUV",
    "4wd": "SUV"
}

class EntityExtractor:
    @staticmethod
    def normalize_digits(text: str) -> str:
        """Converts Bengali numerals to standard ASCII numerals."""
        for b_digit, a_digit in BANGLA_DIGITS.items():
            text = text.replace(b_digit, a_digit)
        return text

    @classmethod
    def extract(cls, text: str, current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Extracts structured entities from multi-lingual user query (English, Bangla, Banglish).
        """
        now = current_time or datetime.now(timezone.utc)
        normalized_text = cls.normalize_digits(text)
        text_lower = normalized_text.lower()

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
            "driver_required": False,
            "is_confirmation": False,
            "is_cancellation": False
        }

        # 1. Extract Locations
        found_locs = []
        for loc_key, loc_name in LOCATION_KEYWORDS.items():
            if re.search(rf"\b{re.escape(loc_key)}\b", text_lower):
                if loc_name not in found_locs:
                    found_locs.append(loc_name)

        entities["locations"] = found_locs

        # Determine pickup vs dropoff if patterns like "Khulna theke Dhaka", "from Khulna to Dhaka", or "Khulna to Dhaka"
        theke_match = re.search(r"([a-zA-Z\u0980-\u09ff\']+)\s+(?:theke|থেকে|from)\s+([a-zA-Z\u0980-\u09ff\']+)(?:\s+(?:te|to|তে))?", text_lower)
        from_to_match = re.search(r"(?:from\s+)?([a-zA-Z\u0980-\u09ff\']+)\s+to\s+([a-zA-Z\u0980-\u09ff\']+)", text_lower)
        route_match = theke_match or from_to_match
        if route_match:
            p_cand, d_cand = route_match.group(1), route_match.group(2)
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
        if ("sonadanga" in text_lower or "সোনাডাঙ্গা" in text_lower) and not entities["pickup_location"]:
            entities["pickup_location"] = "Sonadanga, Khulna"

        # 2. Extract Dates (Bangla, Banglish, Relative, and Specific)
        if re.search(r"\b(agamikal|kalke|kal|tomorrow|আগামীকাল|কালকে|কাল)\b", text_lower):
            target_date = now + timedelta(days=1)
            entities["pickup_date"] = target_date.strftime("%Y-%m-%d")
        elif re.search(r"\b(poroshu|day after tomorrow|পরশু)\b", text_lower):
            target_date = now + timedelta(days=2)
            entities["pickup_date"] = target_date.strftime("%Y-%m-%d")
        elif re.search(r"\b(aaj|ajke|today|আজ|আজকে)\b", text_lower):
            entities["pickup_date"] = now.strftime("%Y-%m-%d")

        tarik_match = re.search(r"\b(\d{1,2})\s*(?:tarik|tarikh|তারিখ|th|st|nd|rd)\b", text_lower)
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

        # 3. Extract Time
        time_match = re.search(
            r"\b(?:sokal|dupur|bikal|shondha|raat|vhor|সকাল|দুপুর|বিকাল|সন্ধ্যা|রাত|ভোর)\s*(\d{1,2})(?::(\d{2}))?\s*(?:tay|ta|am|pm|টায়|টা)?\b|"
            r"\b(\d{1,2})(?::(\d{2}))?\s*(?:am|pm|tay|ta|টায়|টা)\b",
            text_lower
        )
        if time_match:
            match_str = time_match.group(0)
            digits = re.findall(r"\d+", match_str)
            if digits:
                hour = int(digits[0])
                min_str = digits[1] if len(digits) > 1 else "00"
                if any(w in match_str for w in ["shondha", "raat", "bikal", "pm", "সন্ধ্যা", "রাত", "বিকাল"]) and hour < 12:
                    hour += 12
                elif any(w in match_str for w in ["sokal", "am", "vhor", "সকাল", "ভোর"]) and hour == 12:
                    hour = 0
                entities["pickup_time"] = f"{hour:02d}:{min_str}"

        # 4. Extract Vehicle Models & Categories
        for v_key, v_info in VEHICLE_PATTERNS.items():
            if re.search(rf"\b{re.escape(v_key)}\b", text_lower):
                entities["vehicle_name"] = v_info["name"]
                entities["vehicle_id"] = v_info["id"]
                entities["category"] = v_info["category"]
                break

        if not entities["category"]:
            for cat_key, cat_val in CATEGORY_KEYWORDS.items():
                if re.search(rf"\b{re.escape(cat_key)}\b", text_lower):
                    entities["category"] = cat_val
                    break

        # 5. Extract Seats / Passengers (numeric or word format)
        seat_match = re.search(r"(\d+)\s*(?:seat|seater|jon|joner|passenger|person|জন|আসন)", text_lower)
        if seat_match:
            entities["seats"] = int(seat_match.group(1))
        else:
            for w_num, val in WORD_NUMBERS.items():
                if re.search(rf"\b{re.escape(w_num)}\s*(?:seat|seater|jon|joner|passenger|person|জন|আসন)\b", text_lower):
                    entities["seats"] = val
                    break

        # 6. Extract Duration: "3 din", "3 days", "3 diner"
        day_match = re.search(r"(\d+)\s*(?:din|diner|day|days|দিন|দিনের)", text_lower)
        if day_match:
            entities["duration_days"] = int(day_match.group(1))

        # 7. Driver requirement
        if re.search(r"\b(driver\s*soho|with\s*driver|driver\s*lagbe|ড্রাইভার\s*সহ|ড্রাইভার\s*লাগবে)\b", text_lower):
            entities["driver_required"] = True

        # 8. Extract Confirmations / Cancellations
        if re.search(r"\b(haan|ha|yes|confirm|thik\s*ache|proceed|sure|koro|korbo|book\s*it|done|cholo|হ্যাঁ|কনফার্ম|ঠিক\s*আছে)\b", text_lower):
            if not re.search(r"\b(na|cancel|না|বাতিল)\b", text_lower):
                entities["is_confirmation"] = True
        if re.search(r"\b(na|cancel|no|stop|dorkar\s*nai|bad\s*dao|lagbe\s*na|না|বাতিল|দরকার\s*নেই)\b", text_lower):
            entities["is_cancellation"] = True

        return entities

entity_extractor = EntityExtractor()
