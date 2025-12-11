"""Session service."""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.models.conversation import ConversationSession, Message, SessionStatus
from app.schemas.session import SessionCreate, MessageCreate


class SessionService:
    """Service for conversation session operations."""
    
    @staticmethod
    def get_session(db: Session, session_id: int) -> Optional[ConversationSession]:
        """Get session by ID."""
        return db.query(ConversationSession).filter(ConversationSession.id == session_id).first()
    
    @staticmethod
    def get_sessions(db: Session, skip: int = 0, limit: int = 100) -> List[ConversationSession]:
        """Get all sessions."""
        return db.query(ConversationSession).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_patient_sessions(db: Session, patient_id: int) -> List[ConversationSession]:
        """Get all sessions for a patient."""
        return db.query(ConversationSession).filter(ConversationSession.patient_id == patient_id).all()
    
    @staticmethod
    def create_session(db: Session, session_data: SessionCreate) -> ConversationSession:
        """Create a new session."""
        session = ConversationSession(
            **session_data.dict(),
            started_at=datetime.utcnow(),
            status=SessionStatus.ACTIVE
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def add_message(db: Session, message_data: MessageCreate) -> Message:
        """Add a message to a session."""
        message = Message(**message_data.dict())
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def end_session(db: Session, session_id: int) -> Optional[ConversationSession]:
        """End a session."""
        session = SessionService.get_session(db, session_id)
        if not session:
            return None
        
        session.status = SessionStatus.COMPLETED
        session.ended_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
        return session

