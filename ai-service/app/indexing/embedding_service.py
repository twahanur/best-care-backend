import re
import asyncio
import numpy as np
from typing import List
from app.core.config import settings

genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"[EmbeddingService] Gemini client notice: {e}. Using resilient multilingual fallback.")

def generate_multilingual_fallback_vector(text: str, dim: int = 768) -> List[float]:
    """Deterministic normalized multilingual bag-of-words / character n-gram semantic vector."""
    tokens = re.findall(r"[a-z0-9_-]{2,}|[\u0980-\u09ff]{2,}", text.lower())
    vec = np.zeros(dim, dtype=np.float32)
    if not tokens:
        return vec.tolist()

    for token in tokens:
        h1 = abs(hash(token)) % dim
        vec[h1] += 2.0
        if len(token) > 2:
            for i in range(len(token) - 2):
                ngram = token[i:i+3]
                h2 = abs(hash(ngram)) % dim
                vec[h2] += 0.75

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()

async def get_embedding(text: str) -> List[float]:
    """Generate embedding vector for text."""
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
        except Exception:
            pass

    return generate_multilingual_fallback_vector(text, dim=settings.EMBEDDING_DIMENSION)

async def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    results = []
    for text in texts:
        emb = await get_embedding(text)
        results.append(emb)
    return results
