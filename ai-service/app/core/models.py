from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Text, Boolean, Integer, Float, JSON, DateTime, ForeignKey, Index
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.core.config import settings

Base = declarative_base()

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(32), index=True, default="general")
    entity_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    canonical_text: Mapped[str] = mapped_column(Text)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list)
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    chunks: Mapped[List["KnowledgeChunk"]] = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")
    embeddings: Mapped[List["KnowledgeEmbedding"]] = relationship("KnowledgeEmbedding", back_populates="document", cascade="all, delete-orphan")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("knowledge_documents.id", ondelete="CASCADE"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    chunk_text: Mapped[str] = mapped_column(Text)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    document: Mapped["KnowledgeDocument"] = relationship("KnowledgeDocument", back_populates="chunks")
    embeddings: Mapped[List["KnowledgeEmbedding"]] = relationship("KnowledgeEmbedding", back_populates="chunk", cascade="all, delete-orphan")

class KnowledgeEmbedding(Base):
    __tablename__ = "knowledge_embeddings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("knowledge_documents.id", ondelete="CASCADE"), index=True)
    chunk_id: Mapped[str] = mapped_column(String(64), ForeignKey("knowledge_chunks.id", ondelete="CASCADE"), index=True)
    embedding_model: Mapped[str] = mapped_column(String(64), default=settings.EMBEDDING_MODEL)
    embedding_vector: Mapped[List[float]] = mapped_column(Vector(settings.EMBEDDING_DIMENSION))
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", index=True)
    embedded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    document: Mapped["KnowledgeDocument"] = relationship("KnowledgeDocument", back_populates="embeddings")
    chunk: Mapped["KnowledgeChunk"] = relationship("KnowledgeChunk", back_populates="embeddings")

class EmbeddingJob(Base):
    __tablename__ = "embedding_jobs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), index=True)
    action: Mapped[str] = mapped_column(String(32), default="INDEX")
    status: Mapped[str] = mapped_column(String(20), default="PENDING", index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    user_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    user_email: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    user_phone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_role: Mapped[Optional[str]] = mapped_column(String(32), default="CUSTOMER")
    title: Mapped[str] = mapped_column(String(255), default="Car Rental Inquiry Session")
    booking_state_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), ForeignKey("chat_sessions.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20)) # 'user' | 'assistant' | 'system'
    content: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(20), default="english")
    intent: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    query_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    sources_json: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSON, default=list)
    data_json: Mapped[Optional[Any]] = mapped_column(JSON, default=list)
    booking_action_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, index=True)

    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")
