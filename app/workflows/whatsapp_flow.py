"""WhatsApp conversation flow."""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models.conversation import ConversationSession, ConversationTurn
from app.services.ai_service import AIService
from app.services.safety_service import SafetyService
from app.services.escalation_service import EscalationService
from app.workflows.conversation_fsm import ConversationFSM, ConversationState


class WhatsAppFlow:
    """Orchestrator for WhatsApp conversation with natural-language chatbot flow."""
    
    def __init__(self, session: ConversationSession, db: Session):
        self.session = session
        self.db = db
        self.fsm = ConversationFSM(ConversationState.SESSION_START)
        self.ai_service = AIService(db)
        self.safety_service = SafetyService(db)
        self.escalation_service = EscalationService()
        self.turn_counter = 0
    
    async def process_message(self, message: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        """Process incoming WhatsApp message."""
        # Check for opt-out keywords
        if self._is_opt_out(message):
            return self.handle_opt_out()
        
        # Safety check
        safety_check = self.safety_service.check_input(message)
        
        if safety_check["should_escalate"]:
            return await self.handle_emergency(message, safety_check)
        
        # Generate AI response
        history = self._get_conversation_history()
        response = await self.ai_service.generate_response(
            user_input=message,
            current_state=self.fsm.current_state,
            context=self.fsm.context,
            history=history
        )
        
        # Determine next state
        next_state = self._determine_next_state(message, response)
        if next_state:
            self.fsm.transition(next_state)
        
        # Log turn
        self._log_turn(message, response)
        
        # Generate quick replies/buttons
        quick_replies = self._generate_quick_replies()
        
        return {
            "response": response,
            "quick_replies": quick_replies,
            "buttons": self._generate_buttons(),
            "state": self.fsm.current_state.value
        }
    
    def _is_opt_out(self, message: str) -> bool:
        """Check for opt-out keywords."""
        opt_out_keywords = ["stop", "unsubscribe", "cancel", "opt out", "quit"]
        return any(keyword in message.lower() for keyword in opt_out_keywords)
    
    def handle_opt_out(self) -> Dict[str, Any]:
        """Handle opt-out request."""
        # TODO: Update consent record
        return {
            "response": "You have been unsubscribed. Reply 'START' to subscribe again.",
            "opt_out": True
        }
    
    async def handle_emergency(self, message: str, safety_check: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situation."""
        self.fsm.transition(ConversationState.EMERGENCY_FALLBACK)
        
        escalation = self.escalation_service.escalate_to_human(
            self.session,
            reason=safety_check.get("reason"),
            details={"user_input": message}
        )
        
        return {
            "response": "I understand this is an emergency. Please contact emergency services immediately. For medical emergencies, call 193 (Ghana Emergency Services).",
            "escalated": True,
            "state": self.fsm.current_state.value
        }
    
    def _determine_next_state(self, user_input: str, response: str) -> Optional[ConversationState]:
        """Determine next state based on user input."""
        input_lower = user_input.lower()
        state = self.fsm.current_state
        
        if state == ConversationState.SESSION_START:
            return ConversationState.OPT_IN_PROMPT
        elif state == ConversationState.OPT_IN_PROMPT:
            if "yes" in input_lower or "ok" in input_lower or "start" in input_lower:
                self.fsm.context["consent_granted"] = True
                return ConversationState.GREETING
            else:
                return ConversationState.END_SESSION
        elif state == ConversationState.GREETING:
            return ConversationState.TOPIC_INTRO
        elif "next lesson" in input_lower or "continue" in input_lower:
            return ConversationState.DELIVER_LESSON_INTRO
        elif "schedule" in input_lower or "remind" in input_lower:
            return ConversationState.SCHEDULE_OFFER
        
        return None
    
    def _generate_quick_replies(self) -> List[str]:
        """Generate quick reply options."""
        if self.fsm.current_state == ConversationState.SCHEDULE_OFFER:
            return ["Yes, schedule it", "No, thanks", "Maybe later"]
        elif self.fsm.current_state == ConversationState.ENGAGEMENT_CHECK:
            return ["Yes, continue", "No, stop", "Schedule for later"]
        else:
            return ["Next lesson", "Schedule reminder", "Help"]
    
    def _generate_buttons(self) -> List[Dict[str, str]]:
        """Generate button options."""
        buttons = []
        
        if self.fsm.current_state in [ConversationState.DELIVER_LESSON_DETAILED, ConversationState.ENGAGEMENT_CHECK]:
            buttons.append({"type": "reply", "title": "Next Lesson", "id": "next_lesson"})
            buttons.append({"type": "reply", "title": "Schedule", "id": "schedule"})
        
        return buttons
    
    def _get_conversation_history(self) -> list:
        """Get conversation history."""
        turns = self.db.query(ConversationTurn).filter(
            ConversationTurn.session_id == self.session.id
        ).order_by(ConversationTurn.turn_number).all()
        
        return [
            {
                "role": turn.role,
                "content": turn.user_input or turn.assistant_response
            }
            for turn in turns
        ]
    
    def _log_turn(self, user_input: str, assistant_response: str):
        """Log conversation turn."""
        self.turn_counter += 1
        turn = ConversationTurn(
            session_id=self.session.id,
            turn_number=self.turn_counter,
            role="user",
            user_input=user_input,
            assistant_response=assistant_response
        )
        self.db.add(turn)
        self.db.commit()

