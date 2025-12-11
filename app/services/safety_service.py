"""Medical safety guardrails service."""

from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models.safety import AIResponseLog, EscalationRequest, EscalationReason
from app.db.models.conversation import ConversationSession, ConversationTurn


class SafetyService:
    """Service for medical safety guardrails."""
    
    # Safety violation keywords
    DIAGNOSIS_KEYWORDS = [
        "diagnose", "diagnosis", "you have", "you've got", "you're suffering from",
        "you're sick with", "you're infected with"
    ]
    
    MEDICAL_ADVICE_KEYWORDS = [
        "you should take", "you need to", "prescribe", "medication", "treatment",
        "you must", "you have to"
    ]
    
    SYMPTOM_KEYWORDS = [
        "pain", "ache", "bleeding", "fever", "nausea", "vomiting", "dizziness",
        "shortness of breath", "chest pain", "headache", "cramps"
    ]
    
    EMERGENCY_KEYWORDS = [
        "emergency", "urgent", "severe pain", "can't breathe", "unconscious",
        "chest pain", "heart attack", "stroke", "bleeding heavily"
    ]
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_input(self, user_input: str) -> Dict[str, Any]:
        """Check user input for safety violations."""
        input_lower = user_input.lower()
        
        # Check for emergency
        is_emergency = any(keyword in input_lower for keyword in self.EMERGENCY_KEYWORDS)
        if is_emergency:
            return {
                "should_escalate": True,
                "reason": EscalationReason.EMERGENCY,
                "violation_type": "emergency",
                "severity": "critical"
            }
        
        # Check for symptoms mentioned
        has_symptoms = any(keyword in input_lower for keyword in self.SYMPTOM_KEYWORDS)
        if has_symptoms:
            return {
                "should_escalate": True,
                "reason": EscalationReason.SYMPTOMS_MENTIONED,
                "violation_type": "symptoms",
                "severity": "high"
            }
        
        return {
            "should_escalate": False,
            "reason": None,
            "violation_type": None,
            "severity": "low"
        }
    
    def validate_llm_response(self, response: str, session: ConversationSession) -> Dict[str, Any]:
        """Validate LLM response for safety violations."""
        response_lower = response.lower()
        violations = []
        
        # Rule 1: No diagnosis allowed
        if any(keyword in response_lower for keyword in self.DIAGNOSIS_KEYWORDS):
            violations.append({
                "type": "diagnosis",
                "severity": "critical",
                "message": "LLM attempted to provide diagnosis"
            })
            self.log_safety_event(session, "diagnosis_attempted", response)
        
        # Rule 2: No medical advice
        if any(keyword in response_lower for keyword in self.MEDICAL_ADVICE_KEYWORDS):
            violations.append({
                "type": "medical_advice",
                "severity": "high",
                "message": "LLM attempted to provide medical advice"
            })
            self.log_safety_event(session, "medical_advice_attempted", response)
        
        # Rule 3: Check for symptom mentions (should redirect)
        if any(keyword in response_lower for keyword in self.SYMPTOM_KEYWORDS):
            violations.append({
                "type": "symptom_handling",
                "severity": "medium",
                "message": "Response mentions symptoms - should redirect"
            })
        
        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "should_redirect": len(violations) > 0
        }
    
    def log_safety_event(self, session: ConversationSession, event_type: str, details: str):
        """Log safety violation event."""
        from app.db.models.audit import AuditLog
        
        audit_log = AuditLog(
            action=f"safety_violation_{event_type}",
            entity_type="conversation_session",
            entity_id=session.id,
            details={"event_type": event_type, "details": details},
            timestamp=datetime.utcnow()
        )
        self.db.add(audit_log)
        self.db.commit()
    
    def should_escalate(self, conversation_history: List[ConversationTurn]) -> bool:
        """Determine if conversation should be escalated to human."""
        # Escalate if multiple safety violations
        violation_count = sum(1 for turn in conversation_history 
                           if turn.metadata and turn.metadata.get("safety_violation"))
        
        if violation_count >= 2:
            return True
        
        # Escalate if emergency keywords detected
        recent_turns = conversation_history[-3:] if len(conversation_history) >= 3 else conversation_history
        for turn in recent_turns:
            if turn.user_input:
                check = self.check_input(turn.user_input)
                if check["should_escalate"]:
                    return True
        
        return False
    
    def create_escalation_request(self, session: ConversationSession, reason: EscalationReason, 
                                  description: Optional[str] = None) -> EscalationRequest:
        """Create escalation request."""
        escalation = EscalationRequest(
            session_id=session.id,
            patient_id=session.patient_id,
            reason=reason,
            description=description or f"Escalation due to {reason.value}",
            escalated_at=datetime.utcnow()
        )
        self.db.add(escalation)
        self.db.commit()
        self.db.refresh(escalation)
        return escalation

