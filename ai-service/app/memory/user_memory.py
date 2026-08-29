"""
Long-Term User Memory and Preference Store.
Maintains persistent user rental preferences (e.g. favourite vehicle category, seating size, preferred locations).
"""
import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy import select, update
from app.core.database import get_db_session
from app.core.models import UserMemory, get_utc_now

class UserMemoryManager:
    @classmethod
    async def get_user_preferences(cls, user_id: str) -> Dict[str, str]:
        if not user_id:
            return {}

        async with get_db_session() as session:
            result = await session.execute(
                select(UserMemory).where(UserMemory.user_id == user_id)
            )
            records = result.scalars().all()
            return {r.preference_key: r.preference_value for r in records}

    @classmethod
    async def set_preference(cls, user_id: str, key: str, value: str, confidence: float = 1.0):
        if not user_id or not key:
            return

        async with get_db_session() as session:
            result = await session.execute(
                select(UserMemory).where(UserMemory.user_id == user_id, UserMemory.preference_key == key)
            )
            existing = result.scalar_one_or_none()
            if existing:
                existing.preference_value = value
                existing.confidence = confidence
                existing.updated_at = get_utc_now()
            else:
                mem = UserMemory(
                    id=f"umem_{uuid.uuid4().hex[:10]}",
                    user_id=user_id,
                    preference_key=key,
                    preference_value=value,
                    confidence=confidence,
                    created_at=get_utc_now()
                )
                session.add(mem)
            await session.commit()

user_memory = UserMemoryManager()
