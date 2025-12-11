"""Database models."""

from app.db.models.patient import Patient
from app.db.models.hospital import Hospital
from app.db.models.consent import ConsentRecord, ConsentType, ConsentStatus
from app.db.models.schedule_preference import SchedulePreference
from app.db.models.enrollment import EnrollmentSyncLog, SyncStatus
from app.db.models.content import Lesson, Condition, LessonVersion, ContentAsset, LessonVersionStatus
from app.db.models.conversation import ConversationSession, ConversationTurn, CallHistory, SessionStatus
from app.db.models.scheduling import ScheduledCall, CallStatus
from app.db.models.safety import AIResponseLog, EscalationRequest, EscalationReason, EscalationStatus, AuditLog
from app.db.models.auth import User, Role, UserRole

__all__ = [
    # Core
    "Patient",
    "Hospital",
    "ConsentRecord",
    "ConsentType",
    "ConsentStatus",
    "SchedulePreference",
    "EnrollmentSyncLog",
    "SyncStatus",
    # Content
    "Lesson",
    "Condition",
    "LessonVersion",
    "LessonVersionStatus",
    "ContentAsset",
    # Conversation
    "ConversationSession",
    "ConversationTurn",
    "CallHistory",
    "SessionStatus",
    # Scheduling
    "ScheduledCall",
    "CallStatus",
    # Safety & Audit
    "AIResponseLog",
    "EscalationRequest",
    "EscalationReason",
    "EscalationStatus",
    "AuditLog",
    # Auth
    "User",
    "Role",
    "UserRole",
]

