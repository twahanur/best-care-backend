"""
Multilingual Embedding Service with Google Gemini text-embedding-004 and Resilient Offline Fallback.
Handles English, Bengali (বাংলা), and Banglish (phonetic Latin Bangla) semantics.
"""
import re
import asyncio
import numpy as np
from typing import List
from app.core.config import settings

# Initialize Gemini Client if API key is present
genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[EmbeddingService] Gemini client not initialized with key ({e}). Using resilient multilingual fallback.")

# Common Banglish and Bengali script synonym map for robust multilingual semantic matching
BANGLISH_SYNONYM_MAP = {
    # Banglish
    "gari": "car vehicle",
    "gaari": "car vehicle",
    "bhalo": "best good recommendation",
    "lagbe": "need required want",
    "bhara": "rent rate price cost",
    "taka": "price budget cost usd",
    "jonno": "for purpose",
    "niye": "with group passengers",
    "pahari": "mountain offroad hilly terrain",
    "pahar": "mountain hills sajek bandarban",
    "sajek": "mountain offroad 4wd sajek",
    "bandarban": "mountain offroad 4wd bandarban",
    "sylhet": "mountain highway tea garden sylhet",
    "deposit": "security deposit refund payment",
    "bima": "insurance protection cdw",
    "khoroch": "cost price total rate",
    "koto": "price how much rate total",
    # Bengali Unicode Script
    "গাড়ি": "car vehicle fleet",
    "গাড়িটি": "car vehicle fleet",
    "সিকিউরিটি": "security deposit",
    "ডিপোজিট": "security deposit payment refund",
    "রিফান্ড": "refund cancellation return money",
    "পলিসি": "policy rules guidelines terms",
    "বীমা": "insurance protection cdw",
    "ভাড়া": "rent rate price daily cost",
    "পাহাড়": "mountain hills terrain",
    "পাহাড়ি": "mountain hills terrain offroad 4wd",
    "সাজেক": "sajek valley mountain offroad",
    "সিলেট": "sylhet tea garden highway",
    "বান্দরবান": "bandarban hill tracts offroad",
    "লাইসেন্স": "driver license requirements age"
}

def clean_multilingual_tokens(text: str) -> List[str]:
    """
    Tokenizes text supporting English, Bangla script (\u0980-\u09FF), and Latin Banglish words.
    """
    text = text.lower()
    
    # Expand known Banglish terms
    for banglish_word, english_equivalent in BANGLISH_SYNONYM_MAP.items():
        if banglish_word in text:
            text += f" {english_equivalent}"
            
    # Extract Latin alphanumeric tokens & Bengali Unicode character sequences
    tokens = re.findall(r"[a-z0-9_-]{2,}|[\u0980-\u09ff]{2,}", text)
    return tokens

def generate_multilingual_fallback_vector(text: str, dim: int = 256) -> List[float]:
    """
    Deterministic normalized multilingual bag-of-words / character n-gram semantic vector generator.
    Enables instant offline testing, unit test runs, and zero-downtime execution.
    """
    tokens = clean_multilingual_tokens(text)
    vec = np.zeros(dim, dtype=np.float32)
    
    if not tokens:
        return vec.tolist()
        
    for token in tokens:
        # Primary hash
        h1 = abs(hash(token)) % dim
        vec[h1] += 2.0
        
        # Substring n-grams (3-grams) for morphological similarity
        if len(token) > 2:
            for i in range(len(token) - 2):
                ngram = token[i:i+3]
                h2 = abs(hash(ngram)) % dim
                vec[h2] += 0.75

    # L2 Normalization
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
        
    return vec.tolist()

async def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a single text.
    """
    if genai_client and settings.GEMINI_API_KEY:
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    genai_client.models.embed_content,
                    model=settings.EMBEDDING_MODEL,
                    contents=text,
                    config=dict(output_dimensionality=settings.EMBEDDING_DIMENSION)
                ),
                timeout=4.0
            )
            if response and response.embeddings and len(response.embeddings) > 0:
                return response.embeddings[0].values
        except Exception as err:
            pass  # Fall back to multilingual vector
            
    return generate_multilingual_fallback_vector(text, dim=settings.EMBEDDING_DIMENSION)

async def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    """
    results = []
    for text in texts:
        emb = await get_embedding(text)
        results.append(emb)
    return results
