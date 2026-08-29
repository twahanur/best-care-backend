"""
Semantic and Paragraph-Based Text Chunker.
Splits long documents into cohesive semantic chunks with token budgeting and chunk overlaps.
"""
from typing import List, Dict, Any

class DocumentChunker:
    def __init__(self, max_chunk_size: int = 500, overlap: int = 50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Splits text into chunks preserving semantic paragraph boundaries.
        """
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_len = 0
        chunk_idx = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            words = para.split()
            para_len = len(words)

            if current_len + para_len > self.max_chunk_size and current_chunk:
                chunk_str = "\n\n".join(current_chunk)
                chunks.append({
                    "chunk_index": chunk_idx,
                    "chunk_text": chunk_str,
                    "token_count": current_len
                })
                chunk_idx += 1
                current_chunk = [para]
                current_len = para_len
            else:
                current_chunk.append(para)
                current_len += para_len

        if current_chunk:
            chunk_str = "\n\n".join(current_chunk)
            chunks.append({
                "chunk_index": chunk_idx,
                "chunk_text": chunk_str,
                "token_count": current_len
            })

        return chunks if chunks else [{
            "chunk_index": 0,
            "chunk_text": text,
            "token_count": len(text.split())
        }]

chunker = DocumentChunker()
