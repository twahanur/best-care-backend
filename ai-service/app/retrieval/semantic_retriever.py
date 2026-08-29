"""
Semantic Vector Retriever.
Embeds the query at runtime and performs high-speed cosine similarity search over active pgvector/JSON embeddings in PostgreSQL.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument, RAGChunk, RAGEmbedding
from app.indexing.embedding_service import get_embedding
from app.core.config import settings

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (n1 * n2))

class SemanticRetriever:
    @classmethod
    async def retrieve(
        cls,
        query: str,
        top_k: int = 15,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Embeds only user query and computes cosine similarity against pre-computed active database embeddings.
        """
        query_vector = np.array(await get_embedding(query), dtype=np.float32)

        async with get_db_session() as session:
            # Query active embeddings with related document and chunk
            stmt = (
                select(RAGEmbedding)
                .where(RAGEmbedding.status == "ACTIVE")
                .options(
                    selectinload(RAGEmbedding.document),
                    selectinload(RAGEmbedding.chunk)
                )
            )
            result = await session.execute(stmt)
            active_embeddings = result.scalars().all()

            if not active_embeddings:
                from app.indexing.seed_data import seed_knowledge_base_if_empty
                await seed_knowledge_base_if_empty()
                result = await session.execute(stmt)
                active_embeddings = result.scalars().all()

            scored_results = []
            for emb in active_embeddings:
                if not emb.embedding_vector or not emb.document:
                    continue
                
                # Optional category filter
                if category and emb.document.category.lower() != category.lower():
                    continue

                doc_vec = np.array(emb.embedding_vector, dtype=np.float32)
                score = cosine_similarity(query_vector, doc_vec)

                content_text = emb.chunk.chunk_text if emb.chunk else emb.document.content
                scored_results.append({
                    "id": emb.document.id,
                    "chunk_id": emb.chunk_id,
                    "title": emb.document.title,
                    "category": emb.document.category,
                    "content": content_text,
                    "tags": emb.document.tags,
                    "metadata": emb.document.metadata_json,
                    "score": score,
                    "retrieval_type": "semantic"
                })

            scored_results.sort(key=lambda x: x["score"], reverse=True)
            return scored_results[:top_k]

semantic_retriever = SemanticRetriever()
