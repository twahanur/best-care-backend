"""
Query Normalizer and Multilingual Query Expander.
Cleans raw user queries and enhances Banglish / Bengali queries with semantic expansion.
"""
import re
from typing import Dict, Any

BANGLISH_EXPANSIONS = {
    "gari": "car vehicle",
    "gaari": "car vehicle",
    "bhara": "rental rate daily price",
    "koto": "price cost how much",
    "lagbe": "need requirement",
    "dorkar": "need requirement",
    "chai": "want need",
    "pahar": "mountain hills terrain offroad",
    "pahari": "mountainous hilly offroad",
    "sajek": "sajek valley hills mountain 4x4",
    "sylhet": "sylhet tea gardens highway",
    "bandarban": "bandarban hill tracts 4wd",
    "deposit": "security deposit preauthorization refund",
    "bima": "insurance cdw damage protection",
    "family": "family group passengers seats",
    # Bengali Unicode
    "গাড়ি": "car vehicle fleet",
    "সিকিউরিটি": "security deposit",
    "ডিপোজিট": "security deposit refund payment",
    "রিফান্ড": "refund cancellation policy",
    "পলিসি": "policy rules terms",
    "বীমা": "insurance protection cdw",
    "ভাড়া": "rental rate daily price cost",
    "পাহাড়ি": "mountainous terrain offroad",
    "পাহাড়": "mountain hills 4wd",
    "সাজেক": "sajek valley mountain offroad",
    "সিলেট": "sylhet tea garden"
}

class QueryNormalizer:
    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        # Remove repeated punctuation
        cleaned = re.sub(r"[?!.,;:-]+", " ", text)
        cleaned = " ".join(cleaned.split()).strip()
        return cleaned

    @classmethod
    def expand_for_retrieval(cls, text: str) -> str:
        """
        Creates an expanded search string with semantic synonym tags.
        """
        normalized = cls.normalize(text)
        words = normalized.lower().split()
        expanded_terms = []
        
        for w in words:
            if w in BANGLISH_EXPANSIONS:
                expanded_terms.append(BANGLISH_EXPANSIONS[w])
                
        if expanded_terms:
            return f"{normalized} ({' '.join(expanded_terms)})"
        return normalized

query_normalizer = QueryNormalizer()
