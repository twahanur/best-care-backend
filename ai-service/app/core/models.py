"""
Database Models for PostgreSQL RAG Knowledge Base, Embeddings, Jobs, and Conversational Memory.
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class KnowledgeDocument(Base):
    __tablename__ = "rag_documents"

    id = Column(String(128), primary_key=True, index=True)
    entity_type = Column(String(64), nullable=False, default="general", index=True)
    entity_id = Column(String(128), nullable=True, index=True)
    category = Column(String(64), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    canonical_text = Column(Text, nullable=False)
    tags = Column(JSON, nullable=False, default=list)
    metadata_json = Column(JSON, nullable=False, default=dict)
    content_hash = Column(String(64), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    chunks = relationship("RAGChunk", back_populates="document", cascade="all, delete-orphan")
    embeddings = relationship("RAGEmbedding", back_populates="document", cascade="all, delete-orphan")

class RAGChunk(Base):
    __tablename__ = "rag_chunks"

    id = Column(String(128), primary_key=True, index=True)
    document_id = Column(String(128), ForeignKey("rag_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False, default=0)
    chunk_text = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=get_utc_now)

    document = relationship("KnowledgeDocument", back_populates="chunks")
    embeddings = relationship("RAGEmbedding", back_populates="chunk", cascade="all, delete-orphan")

class RAGEmbedding(Base):
    __tablename__ = "rag_embeddings"

    id = Column(String(128), primary_key=True, index=True)
    document_id = Column(String(128), ForeignKey("rag_documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_id = Column(String(128), ForeignKey("rag_chunks.id", ondelete="CASCADE"), nullable=True, index=True)
    embedding_model = Column(String(64), nullable=False)
    embedding_version = Column(String(32), nullable=False, default="v1", index=True)
    embedding_vector = Column(JSON, nullable=False)  # List[float] stored as JSON array for cross-DB compatibility
    status = Column(String(32), nullable=False, default="ACTIVE", index=True)  # ACTIVE, INACTIVE, PENDING
    embedded_at = Column(DateTime, default=get_utc_now)

    document = relationship("KnowledgeDocument", back_populates="embeddings")
    chunk = relationship("RAGChunk", back_populates="embeddings")

class EmbeddingJob(Base):
    __tablename__ = "embedding_jobs"

    id = Column(String(128), primary_key=True, index=True)
    document_id = Column(String(128), nullable=False, index=True)
    action = Column(String(32), default="INDEX")  # INDEX, REINDEX, DELETE
    status = Column(String(32), default="PENDING", index=True)  # PENDING, PROCESSING, COMPLETED, FAILED, RETRYING
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    id = Column(String(128), primary_key=True, index=True)  # session_id
    user_id = Column(String(128), nullable=True, index=True)
    title = Column(String(256), default="New Conversation")
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="ChatMessage.created_at")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(128), primary_key=True, index=True)
    conversation_id = Column(String(128), ForeignKey("chat_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(32), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    language = Column(String(32), default="english")  # english, bangla, banglish, mixed
    intent = Column(String(64), nullable=True)
    sources_json = Column(JSON, default=list)
    matched_vehicles_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=get_utc_now)

    conversation = relationship("ChatConversation", back_populates="messages")

class UserMemory(Base):
    __tablename__ = "user_memories"

    id = Column(String(128), primary_key=True, index=True)
    user_id = Column(String(128), nullable=False, index=True)
    preference_key = Column(String(128), nullable=False)
    preference_value = Column(Text, nullable=False)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
