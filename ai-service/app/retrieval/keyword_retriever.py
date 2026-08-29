"""
Keyword and Lexical Retriever.
Performs lexical search over canonical documents in PostgreSQL.
"""
from typing import List, Dict, Any, Optional
import re
from sqlalchemy import select
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument

class KeywordRetriever:
    @classmethod
    async def retrieve(
        cls,
        query: str,
        top_k: int = 15,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query_terms = set(re.findall(r"\b\w{2,}\b", query.lower()))
        if not query_terms:
            return []

        async with get_db_session() as session:
            stmt = select(KnowledgeDocument).where(KnowledgeDocument.is_active == True)
            if category:
                stmt = stmt.where(KnowledgeDocument.category.ilike(category))
            result = await session.execute(stmt)
            docs = result.scalars().all()

            scored = []
            for doc in docs:
                searchable_text = f"{doc.title} {doc.category} {' '.join(doc.tags or [])} {doc.content}".lower()
                
                # Count keyword hits with weighting
                score = 0.0
                for term in query_terms:
                    if term in doc.title.lower():
                        score += 3.0
                    if term in doc.category.lower():
                        score += 2.0
                    if any(term in tag.lower() for tag in (doc.tags or [])):
                        score += 2.0
                    if term in searchable_text:
                        score += 1.0

                if score > 0:
                    scored.append({
                        "id": doc.id,
                        "chunk_id": None,
                        "title": doc.title,
                        "category": doc.category,
                        "content": doc.content,
                        "tags": doc.tags,
                        "metadata": doc.metadata_json,
                        "score": score,
                        "retrieval_type": "keyword"
                    })

            scored.sort(key=lambda x: x["score"], reverse=True)
            return scored[:top_k]

keyword_retriever = KeywordRetriever()
