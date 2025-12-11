"""Emergency handling flow."""

from typing import Dict, Any
from app.db.models.patient import Patient
from app.services.escalation_service import EscalationService


class EmergencyFlow:
    """Orchestrator for emergency situations."""
    
    def __init__(self, patient: Patient):
        self.patient = patient
        self.escalation_service = EscalationService()
    
    def handle_emergency(self, emergency_details: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emergency situation."""
        # Notify emergency services
        result = self.escalation_service.notify_emergency_services(
            self.patient,
            emergency_details
        )
        
        return {
            "status": "handled",
            "patient_id": self.patient.id,
            "emergency_details": emergency_details,
            "notification_result": result
        }

