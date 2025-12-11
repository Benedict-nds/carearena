"""Conversation models."""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, JSON, Enum, Float
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class SessionStatus(str, enum.Enum):
    """Session status enum."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    ESCALATED = "escalated"


class ConversationSession(BaseModel):
    """Conversation session model."""
    
    __tablename__ = "conversation_sessions"
    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    channel = Column(String, nullable=False)  # ivr, whatsapp, sms
    status = Column(Enum(SessionStatus), default=SessionStatus.ACTIVE)
    current_state = Column(String, nullable=True)  # Current FSM state
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="sessions")
    turns = relationship("ConversationTurn", back_populates="session", cascade="all, delete-orphan")
    call_history = relationship("CallHistory", back_populates="session", cascade="all, delete-orphan", uselist=False)


class ConversationTurn(BaseModel):
    """Conversation turn model (replaces Message for more detailed tracking)."""
    
    __tablename__ = "conversation_turns"
    
    session_id = Column(Integer, ForeignKey("conversation_sessions.id"), nullable=False)
    turn_number = Column(Integer, nullable=False)  # Sequential turn number
    role = Column(String, nullable=False)  # user, assistant, system
    user_input = Column(Text, nullable=True)  # User's input (transcribed)
    assistant_response = Column(Text, nullable=True)  # AI response
    asr_transcript = Column(Text, nullable=True)  # ASR transcript
    audio_url = Column(String, nullable=True)  # Audio file URL
    tts_audio_url = Column(String, nullable=True)  # Generated TTS audio
    latency_ms = Column(Float, nullable=True)  # Response latency in milliseconds
    tokens_used = Column(Integer, nullable=True)  # LLM tokens used
    metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Relationships
    session = relationship("ConversationSession", back_populates="turns")


class CallHistory(BaseModel):
    """Call history model for IVR calls."""
    
    __tablename__ = "call_history"
    
    session_id = Column(Integer, ForeignKey("conversation_sessions.id"), nullable=False, unique=True)
    call_sid = Column(String, nullable=True, index=True)  # Twilio call SID
    phone_number = Column(String, nullable=False)
    call_duration_seconds = Column(Integer, nullable=True)
    call_status = Column(String, nullable=True)  # completed, failed, busy, no-answer
    attempt_number = Column(Integer, default=1)
    retry_count = Column(Integer, default=0)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="call_history")

