"""
Vector Store Compatibility Layer over PostgreSQL pgvector / embeddings.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from app.core.database import get_db_session, init_database_engine
from app.core.models import KnowledgeDocument
from app.indexing.seed_data import seed_knowledge_base_if_empty
from app.retrieval.hybrid_retriever import hybrid_retriever

class VectorStore:
    def __init__(self):
        self.is_initialized: bool = False
        self.documents: List[Dict[str, Any]] = []
        self._embeddings_matrix = None

    @property
    def embeddings_matrix(self):
        if self._embeddings_matrix is None:
            import numpy as np
            self._embeddings_matrix = np.ones((len(self.documents) or 1, 256), dtype=np.float32)
        return self._embeddings_matrix

    async def initialize(self):
        await init_database_engine()
        await seed_knowledge_base_if_empty()
        
        async with get_db_session() as session:
            result = await session.execute(select(KnowledgeDocument).where(KnowledgeDocument.is_active == True))
            docs = result.scalars().all()
            self.documents = [
                {
                    "id": d.id,
                    "category": d.category,
                    "title": d.title,
                    "content": d.content,
                    "tags": d.tags
                }
                for d in docs
            ]
        self.is_initialized = True

    async def search(
        self,
        query: str,
        top_k: int = 4,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if not self.is_initialized:
            await self.initialize()

        candidates = await hybrid_retriever.retrieve(query=query, category=category, top_k=top_k)
        return [
            {
                "id": c["id"],
                "category": c["category"],
                "title": c["title"],
                "content": c["content"],
                "tags": c.get("tags", []),
                "score": c.get("similarity_score", c.get("score", 0.9))
            }
            for c in candidates
        ]

    def get_all_documents(self) -> List[Dict[str, Any]]:
        return self.documents

vector_store = VectorStore()
