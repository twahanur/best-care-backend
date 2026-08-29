"""
Context Builder and Token Budget Manager.
Deduplicates, compresses, and formats grounded evidence context with precise source citations.
"""
from typing import List, Dict, Any

class ContextBuilder:
    @staticmethod
    def build(documents: List[Dict[str, Any]], max_chars: int = 4000) -> str:
        if not documents:
            return "No relevant database documents found."

        seen_docs = set()
        formatted_chunks = []
        total_len = 0

        for i, doc in enumerate(documents, 1):
            doc_id = doc.get("id", f"doc_{i}")
            if doc_id in seen_docs:
                continue
            seen_docs.add(doc_id)

            chunk_text = (
                f"[Source #{i} | {doc.get('category', 'Info')} - {doc.get('title', 'Document')}]\n"
                f"{doc.get('content', '')}"
            )

            if total_len + len(chunk_text) > max_chars and formatted_chunks:
                break

            formatted_chunks.append(chunk_text)
            total_len += len(chunk_text)

        return "\n\n".join(formatted_chunks)

context_builder = ContextBuilder()
