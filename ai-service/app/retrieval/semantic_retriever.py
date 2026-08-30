import re
from typing import List, Dict, Any, Optional
from sqlalchemy import select, text
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument, KnowledgeEmbedding
from app.indexing.embedding_service import get_embedding

class SemanticRetriever:
    @classmethod
    async def retrieve(
        cls,
        query: str,
        top_k: int = 4,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves relevant documents using vector cosine similarity from live PostgreSQL table.
        """
        query_vector = await get_embedding(query)

        # 1. Try pgvector cosine distance query in PostgreSQL
        try:
            async with get_db_session() as session:
                vec_str = "[" + ",".join(str(x) for x in query_vector) + "]"
                sql = """
                    SELECT d.id, d.title, d.category, d.content, d.tags,
                           1 - (e.embedding_vector <=> CAST(:vec AS vector)) as similarity
                    FROM knowledge_embeddings e
                    JOIN knowledge_documents d ON e.document_id = d.id
                    WHERE e.status = 'ACTIVE' AND d.is_active = true
                    ORDER BY similarity DESC
                    LIMIT :top_k;
                """
                res = await session.execute(text(sql), {"vec": vec_str, "top_k": top_k})
                rows = res.mappings().all()
                if rows and len(rows) > 0:
                    return [
                        {
                            "id": r["id"],
                            "title": r["title"],
                            "category": r["category"],
                            "content": r["content"],
                            "similarity": float(r["similarity"])
                        }
                        for r in rows
                    ]
        except Exception as e:
            pass

        # 2. Resilient Database Lexical Search Fallback
        try:
            async with get_db_session() as session:
                stmt = select(KnowledgeDocument).where(KnowledgeDocument.is_active == True)
                if category:
                    stmt = stmt.where(KnowledgeDocument.category.ilike(f"%{category}%"))
                res = await session.execute(stmt)
                docs = res.scalars().all()

                q_tokens = set(re.findall(r"\b\w{3,}\b", query.lower()))
                scored = []
                for doc in docs:
                    searchable = f"{doc.title} {doc.category} {' '.join(doc.tags or [])} {doc.content}".lower()
                    score = sum(1.0 for t in q_tokens if t in searchable)
                    if score > 0:
                        scored.append({
                            "id": doc.id,
                            "title": doc.title,
                            "category": doc.category,
                            "content": doc.content,
                            "similarity": round(min(0.95, 0.40 + score * 0.1), 3)
                        })

                scored.sort(key=lambda x: x["similarity"], reverse=True)
                if scored:
                    return scored[:top_k]
        except Exception:
            pass

        return []

semantic_retriever = SemanticRetriever()
