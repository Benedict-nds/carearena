"""Safety and audit models."""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, JSON, Enum, Float, Boolean
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class EscalationReason(str, enum.Enum):
    """Escalation reason enum."""
    EMERGENCY = "emergency"
    SYMPTOMS_MENTIONED = "symptoms_mentioned"
    MEDICAL_ADVICE_REQUESTED = "medical_advice_requested"
    DIAGNOSIS_REQUESTED = "diagnosis_requested"
    PATIENT_REQUEST = "patient_request"
    SAFETY_VIOLATION = "safety_violation"
    OTHER = "other"


class EscalationStatus(str, enum.Enum):
    """Escalation status enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class AIResponseLog(BaseModel):
    """AI response log for every LLM prompt and output."""
    
    __tablename__ = "ai_response_logs"
    
    session_id = Column(Integer, ForeignKey("conversation_sessions.id"), nullable=True)
    turn_id = Column(Integer, ForeignKey("conversation_turns.id"), nullable=True)
    model_name = Column(String, nullable=False)  # gpt-4o, llama-3, etc.
    prompt = Column(Text, nullable=False)  # Full prompt sent to LLM
    response = Column(Text, nullable=False)  # LLM response
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    latency_ms = Column(Float, nullable=True)  # Latency in milliseconds
    temperature = Column(Float, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    # Relationships
    session = relationship("ConversationSession", foreign_keys=[session_id])
    turn = relationship("ConversationTurn", foreign_keys=[turn_id])


class EscalationRequest(BaseModel):
    """Escalation request model."""
    
    __tablename__ = "escalation_requests"
    
    session_id = Column(Integer, ForeignKey("conversation_sessions.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    reason = Column(Enum(EscalationReason), nullable=False)
    status = Column(Enum(EscalationStatus), default=EscalationStatus.PENDING)
    description = Column(Text, nullable=True)
    escalated_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    session = relationship("ConversationSession", foreign_keys=[session_id])
    patient = relationship("Patient", foreign_keys=[patient_id])
    resolver = relationship("User", foreign_keys=[resolved_by])


class AuditLog(BaseModel):
    """Audit log for system events."""
    
    __tablename__ = "audit_logs"
    
    action = Column(String, nullable=False)  # create, update, delete, approve, etc.
    entity_type = Column(String, nullable=False)  # patient, lesson, session, etc.
    entity_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])

