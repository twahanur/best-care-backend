"""
Conversational Session Memory Manager backed by PostgreSQL.
Persists multi-turn message history and context for Agentic AI reasoning.
"""
from typing import List, Dict, Any, Optional
import uuid
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.core.models import ChatConversation, ChatMessage, get_utc_now
from app.core.config import settings

class ConversationMemory:
    @classmethod
    async def get_or_create_conversation(cls, session_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
        """
        Ensures a conversation record exists in DB and returns the session_id.
        """
        conv_id = session_id or f"session_{uuid.uuid4().hex[:12]}"

        async with get_db_session() as session:
            result = await session.execute(
                select(ChatConversation).where(ChatConversation.id == conv_id)
            )
            conv = result.scalar_one_or_none()
            if not conv:
                conv = ChatConversation(
                    id=conv_id,
                    user_id=user_id,
                    title="Car Rental Inquiry Session",
                    created_at=get_utc_now()
                )
                session.add(conv)
                await session.commit()

        return conv_id

    @classmethod
    async def get_history(cls, session_id: str, max_turns: int = settings.MAX_HISTORY_TURNS) -> List[Dict[str, Any]]:
        """
        Retrieve recent chat messages for a session.
        """
        async with get_db_session() as session:
            stmt = (
                select(ChatMessage)
                .where(ChatMessage.conversation_id == session_id)
                .order_by(ChatMessage.created_at.asc())
            )
            result = await session.execute(stmt)
            messages = result.scalars().all()

            # Take last N turns
            recent = messages[-(max_turns * 2):] if len(messages) > max_turns * 2 else messages

            return [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "language": m.language,
                    "intent": m.intent,
                    "sources": m.sources_json or [],
                    "matched_vehicles": m.matched_vehicles_json or [],
                    "created_at": m.created_at.isoformat() if m.created_at else None
                }
                for m in recent
            ]

    @classmethod
    async def add_message(
        cls,
        session_id: str,
        role: str,
        content: str,
        language: str = "english",
        intent: Optional[str] = None,
        sources: Optional[List[Dict[str, Any]]] = None,
        matched_vehicles: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Persist a message turn to PostgreSQL.
        """
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        await cls.get_or_create_conversation(session_id=session_id)

        async with get_db_session() as session:
            new_msg = ChatMessage(
                id=msg_id,
                conversation_id=session_id,
                role=role,
                content=content,
                language=language,
                intent=intent,
                sources_json=sources or [],
                matched_vehicles_json=matched_vehicles or [],
                created_at=get_utc_now()
            )
            session.add(new_msg)
            await session.commit()

        return msg_id

    @classmethod
    async def clear_history(cls, session_id: str):
        """
        Deletes all messages for a session.
        """
        async with get_db_session() as session:
            await session.execute(
                delete(ChatMessage).where(ChatMessage.conversation_id == session_id)
            )
            await session.commit()

conversation_memory = ConversationMemory()
