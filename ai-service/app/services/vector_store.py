"""
In-Memory Vector Store with Cosine Similarity, Metadata Filtering, and Score Ranking.
"""
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.knowledge_base import KNOWLEDGE_CHUNKS
from app.services.embeddings import get_embedding, get_batch_embeddings

class VectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.embeddings_matrix: Optional[np.ndarray] = None
        self.is_initialized: bool = False

    async def initialize(self):
        """
        Index all knowledge base chunks and precompute their vector embeddings.
        """
        if self.is_initialized:
            return

        self.documents = []
        texts_to_embed = []

        for chunk in KNOWLEDGE_CHUNKS:
            # Combine title, category, tags, and content for rich semantic indexing
            searchable_text = f"Title: {chunk['title']}\nCategory: {chunk['category']}\nTags: {', '.join(chunk['tags'])}\nContent: {chunk['content']}"
            self.documents.append({
                "id": chunk["id"],
                "category": chunk["category"],
                "title": chunk["title"],
                "content": chunk["content"],
                "tags": chunk["tags"],
                "indexed_text": searchable_text
            })
            texts_to_embed.append(searchable_text)

        embeddings_list = await get_batch_embeddings(texts_to_embed)
        self.embeddings_matrix = np.array(embeddings_list, dtype=np.float32)
        self.is_initialized = True
        print(f"[VectorStore] Successfully indexed {len(self.documents)} knowledge base documents.")

    def _cosine_similarity(self, query_vec: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between query vector and all document vectors.
        """
        if self.embeddings_matrix is None or len(self.embeddings_matrix) == 0:
            return np.array([])

        # Ensure query vector is 1D float array
        q = np.asarray(query_vec, dtype=np.float32)
        q_norm = np.linalg.norm(q)
        if q_norm > 0:
            q = q / q_norm

        # Matrix dot product
        doc_norms = np.linalg.norm(self.embeddings_matrix, axis=1)
        doc_norms[doc_norms == 0] = 1.0  # Avoid division by zero
        normalized_matrix = self.embeddings_matrix / doc_norms[:, np.newaxis]

        scores = np.dot(normalized_matrix, q)
        return scores

    async def search(
        self,
        query: str,
        top_k: int = 4,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity search for a given user query.
        """
        if not self.is_initialized:
            await self.initialize()

        query_embedding = await get_embedding(query)
        scores = self._cosine_similarity(np.array(query_embedding))

        results = []
        for idx, score in enumerate(scores):
            doc = self.documents[idx]
            if category and doc["category"].lower() != category.lower():
                continue

            results.append({
                "id": doc["id"],
                "category": doc["category"],
                "title": doc["title"],
                "content": doc["content"],
                "tags": doc["tags"],
                "score": float(score)
            })

        # Sort descending by similarity score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Return all documents indexed in the vector store.
        """
        return self.documents


# Global singleton instance
vector_store = VectorStore()
