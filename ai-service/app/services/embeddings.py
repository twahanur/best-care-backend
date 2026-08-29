"""
Embeddings generation service with Gemini text-embedding-004 and resilient offline fallback.
"""
import math
import re
import numpy as np
from typing import List
from app.core.config import settings

# Attempt to initialize Gemini Client if API key is present
genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[Embeddings] Notice: Gemini client not initialized with key ({e}). Using semantic fallback.")


def _clean_tokens(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"\b[a-z0-9_-]{2,}\b", text)
    return tokens


def _generate_fallback_semantic_vector(text: str, dim: int = 256) -> List[float]:
    """
    Deterministic normalized bag-of-words / character n-gram semantic vector generator.
    Enables instant offline testing, unit test runs, and zero-downtime execution.
    """
    tokens = _clean_tokens(text)
    vec = np.zeros(dim, dtype=np.float32)
    
    if not tokens:
        return vec.tolist()
        
    for token in tokens:
        # Primary hash
        h1 = hash(token) % dim
        vec[h1] += 2.0
        
        # Substring n-grams (3-grams) for morphological similarity
        for i in range(len(token) - 2):
            ngram = token[i:i+3]
            h2 = hash(ngram) % dim
            vec[h2] += 0.5

    # L2 Normalization
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
        
    return vec.tolist()


async def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a given text.
    """
    if genai_client and settings.GEMINI_API_KEY:
        try:
            response = genai_client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text,
            )
            if response.embeddings and len(response.embeddings) > 0:
                embedding = response.embeddings[0].values
                return embedding
        except Exception as err:
            print(f"[Embeddings] Gemini API embedding error: {err}. Falling back to semantic vector.")
            
    return _generate_fallback_semantic_vector(text)


async def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    """
    embeddings = []
    for text in texts:
        emb = await get_embedding(text)
        embeddings.append(emb)
    return embeddings
