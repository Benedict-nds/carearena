"""Escalation service."""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models.patient import Patient
from app.db.models.conversation import ConversationSession, SessionStatus
from app.db.models.safety import EscalationRequest, EscalationReason, EscalationStatus


class EscalationService:
    """Service for handling escalations."""
    
    def __init__(self, db: Optional[Session] = None):
        self.db = db
    
    def escalate_to_human(
        self,
        session: ConversationSession,
        reason: EscalationReason,
        details: Optional[Dict[str, Any]] = None
    ) -> EscalationRequest:
        """Escalate conversation to human agent."""
        if not self.db:
            # Create new session if not provided
            from app.db.database import SessionLocal
            self.db = SessionLocal()
        
        # Create escalation request
        escalation = EscalationRequest(
            session_id=session.id,
            patient_id=session.patient_id,
            reason=reason,
            description=details.get("description") if details else None,
            escalated_at=datetime.utcnow(),
            status=EscalationStatus.PENDING,
            metadata=details
        )
        self.db.add(escalation)
        
        # Update session status
        session.status = SessionStatus.ESCALATED
        self.db.commit()
        self.db.refresh(escalation)
        
        # TODO: Notify human agents (webhook, email, SMS, etc.)
        # self._notify_human_agents(escalation)
        
        return escalation
    
    def notify_emergency_services(self, patient: Patient, emergency_details: Dict[str, Any]) -> Dict[str, Any]:
        """Notify emergency services for critical situations."""
        # TODO: Implement emergency notification logic
        # - Call emergency services API
        # - Send SMS to emergency contacts
        # - Log emergency event
        
        return {
            "status": "notified",
            "patient_id": patient.id,
            "emergency_details": emergency_details,
            "notified_at": datetime.utcnow()
        }
    
    def _notify_human_agents(self, escalation: EscalationRequest):
        """Notify human agents about escalation."""
        # TODO: Implement notification logic
        # - Webhook to agent dashboard
        # - Email notification
        # - SMS alert
        pass

