"""
Intent Detector for Car Rental Domain.
Classifies user queries into distinct retrieval and agent actions.
"""
import re
from typing import Dict, Any

class IntentDetector:
    INTENT_PATTERNS = {
        "TRIP_RECOMMENDATION": [
            r"trip", r"tour", r"vacation", r"travel", r"family", r"going to", r"sajek", r"sylhet",
            r"bandarban", r"hills?", r"mountain", r"off-?road", r"jabo", r"ghum", r"pahar", r"shathe",
            r"luggage", r"passengers?"
        ],
        "POLICY_INQUIRY": [
            r"deposit", r"security", r"refund", r"cancel", r"license", r"age", r"driver",
            r"document", r"mileage", r"fuel", r"full-to-full", r"ferot", r"niyom", r"rules?"
        ],
        "INSURANCE_INQUIRY": [
            r"insurance", r"protection", r"cdw", r"excess", r"deductible", r"roadside", r"bima",
            r"theft", r"accident", r"damage", r"shield"
        ],
        "PRICE_CALCULATION": [
            r"cost", r"how much", r"total", r"koto", r"khoroch", r"price", r"calculate", r"taka",
            r"rate", r"per day", r"diner jonno"
        ],
        "VEHICLE_SEARCH": [
            r"suv", r"sedan", r"van", r"electric", r"ev", r"tesla", r"prado", r"tucson", r"hiace",
            r"camry", r"mercedes", r"mustang", r"automatic", r"seats?", r"7-?seater", r"11-?seater"
        ]
    }

    @classmethod
    def detect(cls, query: str) -> str:
        text = query.lower()
        for intent, patterns in cls.INTENT_PATTERNS.items():
            for p in patterns:
                if re.search(r"\b" + p + r"\b", text) or re.search(p, text):
                    return intent
        return "GENERAL_FAQ"

intent_detector = IntentDetector()
