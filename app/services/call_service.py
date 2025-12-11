"""Outbound call service."""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models.patient import Patient
from app.db.models.scheduling import ScheduledCall, CallStatus
from app.db.models.conversation import CallHistory, ConversationSession, SessionStatus
from app.core.config import settings


class CallService:
    """Service for outbound call operations."""
    
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    
    def initiate_call(self, patient: Patient, scheduled_call: Optional[ScheduledCall] = None) -> dict:
        """Initiate an outbound call to a patient."""
        if not self.db:
            from app.db.database import SessionLocal
            self.db = SessionLocal()
        
        try:
            # TODO: Integrate with Twilio
            # from twilio.rest import Client
            # client = Client(self.twilio_account_sid, self.twilio_auth_token)
            # 
            # call = client.calls.create(
            #     url=f"{settings.APP_URL}/api/v1/ivr/voice",
            #     to=patient.phone_number,
            #     from_=settings.TWILIO_PHONE_NUMBER
            # )
            
            # Create call history
            session = ConversationSession(
                patient_id=patient.id,
                channel="ivr",
                status=SessionStatus.ACTIVE,
                started_at=datetime.utcnow()
            )
            self.db.add(session)
            self.db.commit()
            
            call_history = CallHistory(
                session_id=session.id,
                phone_number=patient.phone_number,
                call_sid=None,  # call.sid when Twilio integrated
                call_status="initiated",
                attempt_number=1,
                started_at=datetime.utcnow()
            )
            self.db.add(call_history)
            
            if scheduled_call:
                scheduled_call.status = CallStatus.IN_PROGRESS
                scheduled_call.call_history = call_history
            
            self.db.commit()
            
            return {
                "status": "initiated",
                "call_sid": None,  # call.sid when Twilio integrated
                "patient_id": patient.id,
                "session_id": session.id
            }
        except Exception as e:
            if scheduled_call:
                scheduled_call.status = CallStatus.FAILED
                self.db.commit()
            raise e
    
    def handle_call_status_update(self, call_sid: str, status: str) -> dict:
        """Handle call status updates from telephony provider."""
        if not self.db:
            from app.db.database import SessionLocal
            self.db = SessionLocal()
        
        call_history = self.db.query(CallHistory).filter(
            CallHistory.call_sid == call_sid
        ).first()
        
        if call_history:
            call_history.call_status = status
            call_history.ended_at = datetime.utcnow()
            
            # Update session status
            if status in ["completed", "failed", "no-answer", "busy"]:
                call_history.session.status = SessionStatus.COMPLETED
                call_history.session.ended_at = datetime.utcnow()
            
            self.db.commit()
        
        return {
            "call_sid": call_sid,
            "status": status
        }

