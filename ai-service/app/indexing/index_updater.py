"""
Atomic Index Updater and Embedding Version Manager.
Manages atomic activation (ACTIVE/INACTIVE status) and index consistency.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import KnowledgeDocument, RAGChunk, RAGEmbedding, get_utc_now
from app.core.config import settings

class IndexUpdater:
    @staticmethod
    async def index_document_chunks(
        session: AsyncSession,
        document_id: str,
        chunks_data: List[Dict[str, Any]],
        embeddings: List[List[float]],
        version: str = settings.EMBEDDING_VERSION,
        model_name: str = settings.EMBEDDING_MODEL
    ):
        """
        Atomically saves chunks and activates new embeddings while archiving old versions.
        """
        # 1. Archive existing ACTIVE embeddings for this document
        await session.execute(
            update(RAGEmbedding)
            .where(RAGEmbedding.document_id == document_id, RAGEmbedding.status == "ACTIVE")
            .values(status="INACTIVE")
        )

        # 2. Delete previous chunks if re-indexing
        await session.execute(
            delete(RAGChunk).where(RAGChunk.document_id == document_id)
        )

        # 3. Insert new chunks and active embeddings
        for i, chunk_info in enumerate(chunks_data):
            chunk_id = f"chk_{document_id}_{i}_{uuid.uuid4().hex[:6]}"
            new_chunk = RAGChunk(
                id=chunk_id,
                document_id=document_id,
                chunk_index=chunk_info.get("chunk_index", i),
                chunk_text=chunk_info.get("chunk_text", ""),
                token_count=chunk_info.get("token_count", 0),
                created_at=get_utc_now()
            )
            session.add(new_chunk)

            emb_id = f"emb_{document_id}_{i}_{uuid.uuid4().hex[:6]}"
            vector = embeddings[i] if i < len(embeddings) else []
            new_embedding = RAGEmbedding(
                id=emb_id,
                document_id=document_id,
                chunk_id=chunk_id,
                embedding_model=model_name,
                embedding_version=version,
                embedding_vector=vector,
                status="ACTIVE",
                embedded_at=get_utc_now()
            )
            session.add(new_embedding)

        await session.commit()
