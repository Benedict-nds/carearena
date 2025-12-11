"""SMS conversation flow."""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models.conversation import ConversationSession, ConversationTurn
from app.db.models.content import Lesson
from app.services.ai_service import AIService
from app.services.safety_service import SafetyService
from app.services.escalation_service import EscalationService


class SMSFlow:
    """Orchestrator for SMS conversation - short text delivery of approved lesson snippets."""
    
    def __init__(self, session: ConversationSession, db: Session):
        self.session = session
        self.db = db
        self.ai_service = AIService(db)
        self.safety_service = SafetyService(db)
        self.escalation_service = EscalationService()
        self.turn_counter = 0
    
    async def send_lesson_snippet(self, lesson_id: int) -> Dict[str, Any]:
        """Send approved lesson snippet via SMS."""
        lesson = self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        if not lesson or not lesson.is_active:
            return {"error": "Lesson not found or inactive"}
        
        # Get approved version
        approved_version = None
        for version in lesson.versions:
            if version.status.value == "approved":
                approved_version = version
                break
        
        content = approved_version.content if approved_version else lesson.content
        
        # Truncate to SMS-friendly length (160 chars)
        snippet = self._truncate_for_sms(content, max_length=150)
        
        # Send SMS
        result = await self._send_sms(snippet)
        
        # Log turn
        self._log_turn(None, snippet, lesson_id=lesson_id)
        
        return {
            "message": snippet,
            "lesson_id": lesson_id,
            "sent": result.get("success", False)
        }
    
    async def process_incoming_message(self, message: str) -> Dict[str, Any]:
        """Process incoming SMS message."""
        # Check for opt-out keywords
        if self._is_opt_out(message):
            return self.handle_opt_out()
        
        # Check for acknowledgment keywords
        if self._is_acknowledgment(message):
            return {"response": "Thank you for confirming!"}
        
        # Safety check
        safety_check = self.safety_service.check_input(message)
        
        if safety_check["should_escalate"]:
            return await self.handle_emergency(message, safety_check)
        
        # Generate short response
        response = await self._generate_short_response(message)
        
        # Log turn
        self._log_turn(message, response)
        
        return {
            "response": response
        }
    
    def _is_opt_out(self, message: str) -> bool:
        """Check for opt-out keywords."""
        opt_out_keywords = ["stop", "unsubscribe", "cancel", "opt out", "quit", "end"]
        return any(keyword in message.lower() for keyword in opt_out_keywords)
    
    def _is_acknowledgment(self, message: str) -> bool:
        """Check for acknowledgment keywords."""
        ack_keywords = ["ok", "okay", "yes", "received", "thanks", "thank you"]
        return any(keyword in message.lower() for keyword in ack_keywords)
    
    def handle_opt_out(self) -> Dict[str, Any]:
        """Handle opt-out request."""
        # TODO: Update consent record
        return {
            "response": "You have been unsubscribed. Reply 'START' to subscribe again.",
            "opt_out": True
        }
    
    async def handle_emergency(self, message: str, safety_check: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situation."""
        escalation = self.escalation_service.escalate_to_human(
            self.session,
            reason=safety_check.get("reason"),
            details={"user_input": message}
        )
        
        return {
            "response": "EMERGENCY: Please contact emergency services at 193 (Ghana Emergency Services) immediately.",
            "escalated": True
        }
    
    async def _generate_short_response(self, user_input: str) -> str:
        """Generate short SMS-friendly response."""
        # Keep responses under 160 characters
        response = await self.ai_service.generate_response(
            user_input=user_input,
            current_state=None,  # SMS doesn't use FSM
            context={},
            history=[]
        )
        
        return self._truncate_for_sms(response, max_length=150)
    
    def _truncate_for_sms(self, text: str, max_length: int = 160) -> str:
        """Truncate text to SMS-friendly length."""
        if len(text) <= max_length:
            return text
        
        # Truncate at word boundary
        truncated = text[:max_length-3]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    async def _send_sms(self, message: str) -> Dict[str, Any]:
        """Send SMS via Twilio or other provider."""
        # TODO: Integrate with Twilio
        # from twilio.rest import Client
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # message = client.messages.create(
        #     body=message,
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=self.session.patient.phone_number
        # )
        # return {"success": True, "message_sid": message.sid}
        
        return {"success": True}
    
    def _log_turn(self, user_input: Optional[str], assistant_response: str, lesson_id: Optional[int] = None):
        """Log conversation turn."""
        self.turn_counter += 1
        turn = ConversationTurn(
            session_id=self.session.id,
            turn_number=self.turn_counter,
            role="user" if user_input else "assistant",
            user_input=user_input,
            assistant_response=assistant_response,
            metadata={"lesson_id": lesson_id} if lesson_id else None
        )
        self.db.add(turn)
        self.db.commit()

