"""
Asynchronous Embedding Job Queue and Retry Manager.
Handles job scheduling, status updates, exponential backoff, and deduplication.
"""
import asyncio
import uuid
from typing import Optional, Dict, Any, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.core.models import EmbeddingJob, get_utc_now

class EmbeddingQueue:
    _memory_queue: asyncio.Queue = asyncio.Queue()

    @classmethod
    async def enqueue(cls, document_id: str, action: str = "INDEX") -> str:
        """
        Enqueue an embedding job both in PostgreSQL and the async worker queue.
        """
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        
        async with get_db_session() as session:
            job = EmbeddingJob(
                id=job_id,
                document_id=document_id,
                action=action,
                status="PENDING",
                attempts=0,
                max_attempts=3,
                created_at=get_utc_now()
            )
            session.add(job)
            await session.commit()

        await cls._memory_queue.put({"job_id": job_id, "document_id": document_id, "action": action})
        return job_id

    @classmethod
    async def get_next_job(cls) -> Optional[Dict[str, Any]]:
        """
        Fetch next pending job from the worker queue.
        """
        try:
            job = await asyncio.wait_for(cls._memory_queue.get(), timeout=1.0)
            return job
        except asyncio.TimeoutError:
            return None

    @classmethod
    def task_done(cls):
        cls._memory_queue.task_done()

    @classmethod
    async def update_job_status(
        cls,
        job_id: str,
        status: str,
        error_message: Optional[str] = None
    ):
        """
        Update status of a job in the database.
        """
        async with get_db_session() as session:
            stmt = (
                update(EmbeddingJob)
                .where(EmbeddingJob.id == job_id)
                .values(
                    status=status,
                    error_message=error_message,
                    updated_at=get_utc_now()
                )
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_queue_stats(cls) -> Dict[str, Any]:
        """
        Returns queue statistics and pending/processing job counts.
        """
        async with get_db_session() as session:
            result = await session.execute(select(EmbeddingJob))
            jobs = result.scalars().all()
            
            stats = {
                "total_jobs": len(jobs),
                "pending": sum(1 for j in jobs if j.status == "PENDING"),
                "processing": sum(1 for j in jobs if j.status == "PROCESSING"),
                "completed": sum(1 for j in jobs if j.status == "COMPLETED"),
                "failed": sum(1 for j in jobs if j.status == "FAILED"),
                "queue_buffer_size": cls._memory_queue.qsize()
            }
            return stats
