"""
Hybrid Retriever with Reciprocal Rank Fusion (RRF).
Merges semantic vector retrieval and lexical keyword retrieval for high recall and precision.
"""
from typing import List, Dict, Any, Optional
from app.retrieval.semantic_retriever import semantic_retriever
from app.retrieval.keyword_retriever import keyword_retriever
from app.retrieval.metadata_filter import metadata_filter
from app.core.config import settings

class HybridRetriever:
    @classmethod
    async def retrieve(
        cls,
        query: str,
        category: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        # 1. Parallel / sequential execution of semantic and keyword search
        semantic_docs = await semantic_retriever.retrieve(query, top_k=settings.MAX_CANDIDATES, category=category)
        keyword_docs = await keyword_retriever.retrieve(query, top_k=settings.MAX_CANDIDATES, category=category)

        # 2. Compute RRF scores
        rrf_k = settings.RRF_K
        doc_map: Dict[str, Dict[str, Any]] = {}
        rrf_scores: Dict[str, float] = {}

        for rank, doc in enumerate(semantic_docs, 1):
            doc_id = doc["id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank))

        for rank, doc in enumerate(keyword_docs, 1):
            doc_id = doc["id"]
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank))

        # 3. Assemble merged candidates
        merged_candidates = []
        for doc_id, doc in doc_map.items():
            candidate = dict(doc)
            candidate["rrf_score"] = rrf_scores[doc_id]
            candidate["similarity_score"] = doc.get("score", 0.0)
            merged_candidates.append(candidate)

        # Sort by RRF score descending
        merged_candidates.sort(key=lambda x: x["rrf_score"], reverse=True)

        # 4. Apply metadata filtering if constraints are present
        if constraints:
            merged_candidates = metadata_filter.apply(merged_candidates, constraints)

        return merged_candidates[:top_k]

hybrid_retriever = HybridRetriever()
