import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy import select, update, delete
from app.core.database import get_db_session
from app.core.models import ChatSession, ChatMessage, get_utc_now
from app.core.config import settings

# In-memory session and message cache fallback
_SESSION_CACHE: Dict[str, Dict[str, Any]] = {}
_MESSAGE_CACHE: Dict[str, List[Dict[str, Any]]] = {}

class ConversationMemory:
    @classmethod
    async def get_or_create_session(
        cls,
        session_id: Optional[str] = None,
        user_info: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Gets existing session from DB or creates a new one.
        """
        sid = session_id or f"session_{uuid.uuid4().hex[:12]}"
        user_info = user_info or {}

        try:
            async with get_db_session() as db_session:
                result = await db_session.execute(
                    select(ChatSession).where(ChatSession.id == sid)
                )
                chat_sess = result.scalar_one_or_none()
                if not chat_sess:
                    chat_sess = ChatSession(
                        id=sid,
                        user_id=user_info.get("id") or user_info.get("userId"),
                        user_name=user_info.get("name"),
                        user_email=user_info.get("email"),
                        user_phone=user_info.get("phone"),
                        user_role=user_info.get("role", "CUSTOMER"),
                        title="Car Rental Session",
                        booking_state_json={},
                        metadata_json={},
                        created_at=get_utc_now()
                    )
                    db_session.add(chat_sess)
                    await db_session.commit()
                    await db_session.refresh(chat_sess)

                return chat_sess
        except Exception:
            # Resilient in-memory fallback
            if sid not in _SESSION_CACHE:
                _SESSION_CACHE[sid] = {
                    "id": sid,
                    "user_id": user_info.get("id"),
                    "booking_state_json": {},
                    "user_role": user_info.get("role", "CUSTOMER")
                }
            
            class MockSession:
                id = sid
                booking_state_json = _SESSION_CACHE[sid].get("booking_state_json", {})
            return MockSession()

    @classmethod
    async def get_session_state(cls, session_id: str) -> Dict[str, Any]:
        """Retrieve booking state and session metadata."""
        try:
            async with get_db_session() as db_session:
                result = await db_session.execute(
                    select(ChatSession).where(ChatSession.id == session_id)
                )
                sess = result.scalar_one_or_none()
                if sess and sess.booking_state_json:
                    return dict(sess.booking_state_json)
        except Exception:
            pass

        return _SESSION_CACHE.get(session_id, {}).get("booking_state_json", {})

    @classmethod
    async def save_session_state(cls, session_id: str, state_dict: Dict[str, Any]):
        """Save booking state to session record."""
        if session_id not in _SESSION_CACHE:
            _SESSION_CACHE[session_id] = {}
        _SESSION_CACHE[session_id]["booking_state_json"] = state_dict

        try:
            async with get_db_session() as db_session:
                await db_session.execute(
                    update(ChatSession)
                    .where(ChatSession.id == session_id)
                    .values(booking_state_json=state_dict, updated_at=get_utc_now())
                )
                await db_session.commit()
        except Exception:
            pass

    @classmethod
    async def get_history(cls, session_id: str, max_turns: int = settings.MAX_HISTORY_TURNS) -> List[Dict[str, Any]]:
        """Retrieve recent message history."""
        try:
            async with get_db_session() as db_session:
                stmt = (
                    select(ChatMessage)
                    .where(ChatMessage.session_id == session_id)
                    .order_by(ChatMessage.created_at.asc())
                )
                result = await db_session.execute(stmt)
                messages = result.scalars().all()
                recent = messages[-(max_turns * 2):] if len(messages) > max_turns * 2 else messages

                return [
                    {
                        "id": m.id,
                        "role": m.role,
                        "content": m.content,
                        "language": m.language,
                        "intent": m.intent,
                        "query_type": m.query_type,
                        "created_at": m.created_at.isoformat() if m.created_at else None
                    }
                    for m in recent
                ]
        except Exception:
            return _MESSAGE_CACHE.get(session_id, [])

    @classmethod
    async def add_message(
        cls,
        session_id: str,
        role: str,
        content: str,
        language: str = "english",
        intent: Optional[str] = None,
        query_type: Optional[str] = None,
        sources: Optional[List[Dict[str, Any]]] = None,
        data: Optional[Any] = None,
        booking_action: Optional[Dict[str, Any]] = None
    ) -> str:
        """Persist message turn in PostgreSQL and memory cache."""
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        msg_dict = {
            "id": msg_id,
            "session_id": session_id,
            "role": role,
            "content": content,
            "language": language,
            "intent": intent,
            "query_type": query_type,
            "sources": sources or [],
            "data": data or [],
            "booking_action": booking_action,
            "created_at": get_utc_now().isoformat()
        }
        if session_id not in _MESSAGE_CACHE:
            _MESSAGE_CACHE[session_id] = []
        _MESSAGE_CACHE[session_id].append(msg_dict)

        try:
            async with get_db_session() as db_session:
                msg = ChatMessage(
                    id=msg_id,
                    session_id=session_id,
                    role=role,
                    content=content,
                    language=language,
                    intent=intent,
                    query_type=query_type,
                    sources_json=sources or [],
                    data_json=data or [],
                    booking_action_json=booking_action,
                    created_at=get_utc_now()
                )
                db_session.add(msg)
                await db_session.commit()
        except Exception:
            pass

        return msg_id

conversation_memory = ConversationMemory()
