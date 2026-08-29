"""
Non-Blocking Background Embedding Worker.
Continuously consumes embedding jobs from the queue and updates vector embeddings in PostgreSQL.
"""
import asyncio
import traceback
from typing import Optional
from sqlalchemy import select
from app.core.database import get_db_session
from app.core.models import KnowledgeDocument
from app.indexing.chunker import chunker
from app.indexing.embedding_service import get_batch_embeddings
from app.indexing.index_updater import IndexUpdater
from app.workers.embedding_queue import EmbeddingQueue

class BackgroundEmbeddingWorker:
    def __init__(self, worker_id: int = 1):
        self.worker_id = worker_id
        self._is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """
        Start worker loop in an asyncio task.
        """
        if self._is_running:
            return
        self._is_running = True
        self._task = asyncio.create_task(self._run_loop())
        print(f"[Worker #{self.worker_id}] Background embedding worker started.")

    async def stop(self):
        """
        Stop worker loop gracefully.
        """
        self._is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        print(f"[Worker #{self.worker_id}] Background embedding worker stopped.")

    async def _process_single_document(self, document_id: str):
        """
        Fetch document from DB, build chunks, generate embeddings, and update pgvector index.
        """
        async with get_db_session() as session:
            result = await session.execute(
                select(KnowledgeDocument).where(KnowledgeDocument.id == document_id)
            )
            doc = result.scalar_one_or_none()
            if not doc:
                print(f"[Worker #{self.worker_id}] Document {document_id} not found in DB.")
                return

            text_to_embed = doc.canonical_text or doc.content
            chunks = chunker.chunk_text(text_to_embed)
            chunk_texts = [c["chunk_text"] for c in chunks]

            embeddings = await get_batch_embeddings(chunk_texts)
            await IndexUpdater.index_document_chunks(
                session=session,
                document_id=document_id,
                chunks_data=chunks,
                embeddings=embeddings
            )
            print(f"[Worker #{self.worker_id}] Indexed document '{doc.title}' ({len(chunks)} chunks).")

    async def _run_loop(self):
        while self._is_running:
            try:
                job = await EmbeddingQueue.get_next_job()
                if job is None:
                    await asyncio.sleep(0.5)
                    continue

                job_id = job["job_id"]
                document_id = job["document_id"]
                action = job.get("action", "INDEX")

                await EmbeddingQueue.update_job_status(job_id, "PROCESSING")

                try:
                    if action in ["INDEX", "REINDEX"]:
                        await self._process_single_document(document_id)
                    await EmbeddingQueue.update_job_status(job_id, "COMPLETED")
                except Exception as err:
                    print(f"[Worker #{self.worker_id}] Error processing job {job_id}: {err}")
                    traceback.print_exc()
                    await EmbeddingQueue.update_job_status(job_id, "FAILED", error_message=str(err))
                finally:
                    EmbeddingQueue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Worker #{self.worker_id}] Unexpected error in worker loop: {e}")
                await asyncio.sleep(1.0)

# Global background worker instance
background_worker = BackgroundEmbeddingWorker()
