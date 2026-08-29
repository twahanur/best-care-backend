"""
Multilingual Language Detector.
Identifies whether user input is English, Bengali script (বাংলা), Banglish (phonetic Latin), or Mixed.
"""
import re

BANGLISH_MARKERS = {
    "amar", "amader", "apnader", "koto", "lagbe", "gari", "gaari", "bhara", "jonno",
    "niye", "jabo", "korte", "hobe", "pahar", "pahari", "sajek", "sylhet", "taka",
    "ache", "thakbe", "bhalo", "chai", "dorkar", "khujchi", "dekhun", "bolun", "din",
    "diner", "kivabe", "kotodur", "bima", "shathe", "shob", "ekta"
}

class LanguageDetector:
    @staticmethod
    def detect(text: str) -> str:
        if not text or not text.strip():
            return "english"

        cleaned = text.strip().lower()
        words = re.findall(r"\b[a-z0-9_'-]+\b|[\u0980-\u09ff]+", cleaned)
        
        has_bengali_script = bool(re.search(r"[\u0980-\u09ff]", cleaned))
        has_latin_script = bool(re.search(r"[a-z]", cleaned))

        # Check for Banglish vocabulary
        banglish_hits = sum(1 for w in words if w in BANGLISH_MARKERS)
        
        if has_bengali_script and has_latin_script:
            return "mixed"
        elif has_bengali_script:
            return "bangla"
        elif banglish_hits >= 1 or (len(words) > 0 and (banglish_hits / len(words)) >= 0.15):
            return "banglish"
        else:
            return "english"

language_detector = LanguageDetector()
