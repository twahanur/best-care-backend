"""
Embeddings Compatibility Layer.
Routes to multilingual embedding service with Gemini text-embedding-004 and fallback.
"""
from typing import List
from app.indexing.embedding_service import get_embedding, get_batch_embeddings

__all__ = ["get_embedding", "get_batch_embeddings"]
