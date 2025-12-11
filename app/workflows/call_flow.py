"""Orchestrator for IVR conversation flow - ASR → LLM → TTS pipeline."""

from typing import Dict, Any, Optional
from datetime import datetime
from app.workflows.conversation_fsm import ConversationFSM, ConversationState
from app.db.models.conversation import ConversationSession, ConversationTurn
from app.services.ai_service import AIService
from app.services.safety_service import SafetyService
from app.services.escalation_service import EscalationService
from sqlalchemy.orm import Session


class CallFlow:
    """Orchestrator for IVR conversation with ASR → LLM → TTS pipeline."""
    
    def __init__(self, session: ConversationSession, db: Session):
        self.session = session
        self.db = db
        self.fsm = ConversationFSM(ConversationState.SESSION_START)
        self.ai_service = AIService()
        self.safety_service = SafetyService()
        self.escalation_service = EscalationService()
        self.turn_counter = 0
    
    async def process_audio_input(self, audio_url: str) -> Dict[str, Any]:
        """Process audio input through ASR → LLM → TTS pipeline."""
        start_time = datetime.utcnow()
        
        # Step 1: ASR - Transcribe audio to text
        user_input = await self.ai_service.transcribe_audio(audio_url)
        
        # Step 2: Safety check
        safety_check = self.safety_service.check_input(user_input)
        
        if safety_check["should_escalate"]:
            return await self.handle_emergency(user_input, safety_check)
        
        # Step 3: Process based on current state
        response_data = await self.process_user_input(user_input)
        
        # Step 4: Generate TTS audio
        tts_audio_url = await self.ai_service.synthesize_speech(
            response_data["response"],
            language=self.session.patient.language_preference
        )
        
        # Step 5: Log turn
        latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.log_turn(user_input, response_data["response"], audio_url, tts_audio_url, latency_ms)
        
        return {
            **response_data,
            "tts_audio_url": tts_audio_url,
            "latency_ms": latency_ms
        }
    
    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and generate response."""
        # Get conversation history
        history = self.get_conversation_history()
        
        # Generate AI response based on current state
        response = await self.ai_service.generate_response(
            user_input=user_input,
            current_state=self.fsm.current_state,
            context=self.fsm.context,
            history=history
        )
        
        # Process state transitions based on response
        next_state = self.determine_next_state(user_input, response)
        if next_state:
            self.fsm.transition(next_state)
        
        # Update session state
        self.session.current_state = self.fsm.current_state.value
        self.db.commit()
        
        return {
            "response": response,
            "state": self.fsm.current_state.value
        }
    
    def determine_next_state(self, user_input: str, response: str) -> Optional[ConversationState]:
        """Determine next state based on user input and current state."""
        state = self.fsm.current_state
        
        if state == ConversationState.SESSION_START:
            return ConversationState.OPT_IN_PROMPT
        elif state == ConversationState.OPT_IN_PROMPT:
            if "yes" in user_input.lower() or "ok" in user_input.lower():
                self.fsm.context["consent_granted"] = True
                return ConversationState.GREETING
            else:
                return ConversationState.END_SESSION
        elif state == ConversationState.GREETING:
            return ConversationState.TOPIC_INTRO
        elif state == ConversationState.TOPIC_INTRO:
            return ConversationState.DELIVER_LESSON_INTRO
        elif state == ConversationState.DELIVER_LESSON_INTRO:
            return ConversationState.DELIVER_LESSON_BRIEF
        elif state == ConversationState.DELIVER_LESSON_BRIEF:
            return ConversationState.ENGAGEMENT_CHECK
        elif state == ConversationState.ENGAGEMENT_CHECK:
            if "yes" in user_input.lower() or "continue" in user_input.lower():
                return ConversationState.DELIVER_LESSON_DETAILED
            else:
                return ConversationState.SCHEDULE_OFFER
        elif state == ConversationState.DELIVER_LESSON_DETAILED:
            return ConversationState.SCHEDULE_OFFER
        elif state == ConversationState.SCHEDULE_OFFER:
            if "yes" in user_input.lower():
                return ConversationState.CONFIRM_SCHEDULE
            else:
                return ConversationState.END_SESSION
        elif state == ConversationState.CONFIRM_SCHEDULE:
            return ConversationState.END_SESSION
        
        return None
    
    async def handle_emergency(self, user_input: str, safety_check: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situation."""
        self.fsm.transition(ConversationState.EMERGENCY_FALLBACK)
        
        # Create escalation request
        escalation = self.escalation_service.escalate_to_human(
            self.session,
            reason=safety_check.get("reason", "emergency"),
            details={"user_input": user_input}
        )
        
        response = "I understand this is an emergency. Please stay on the line while I connect you with emergency services."
        tts_audio_url = await self.ai_service.synthesize_speech(
            response,
            language=self.session.patient.language_preference
        )
        
        self.log_turn(user_input, response, None, tts_audio_url, 0)
        
        return {
            "response": response,
            "state": self.fsm.current_state.value,
            "escalated": True,
            "tts_audio_url": tts_audio_url
        }
    
    def get_conversation_history(self) -> list:
        """Get conversation history for context."""
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
    
    def log_turn(self, user_input: str, assistant_response: str, audio_url: Optional[str], 
                 tts_audio_url: Optional[str], latency_ms: float):
        """Log conversation turn."""
        self.turn_counter += 1
        turn = ConversationTurn(
            session_id=self.session.id,
            turn_number=self.turn_counter,
            role="user",
            user_input=user_input,
            assistant_response=assistant_response,
            audio_url=audio_url,
            tts_audio_url=tts_audio_url,
            latency_ms=latency_ms
        )
        self.db.add(turn)
        self.db.commit()

