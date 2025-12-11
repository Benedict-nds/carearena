"""Conversation finite state machine for voice agent."""

from enum import Enum
from typing import Optional, Dict, Any


class ConversationState(str, Enum):
    """All states for voice agent conversation."""
    SESSION_START = "session_start"
    OPT_IN_PROMPT = "opt_in_prompt"
    GREETING = "greeting"
    TOPIC_INTRO = "topic_intro"
    DELIVER_LESSON_INTRO = "deliver_lesson_intro"
    DELIVER_LESSON_BRIEF = "deliver_lesson_brief"
    DELIVER_LESSON_DETAILED = "deliver_lesson_detailed"
    ENGAGEMENT_CHECK = "engagement_check"
    SCHEDULE_OFFER = "schedule_offer"
    CONFIRM_SCHEDULE = "confirm_schedule"
    SAFE_REDIRECT = "safe_redirect"
    EMERGENCY_FALLBACK = "emergency_fallback"
    END_SESSION = "end_session"


class ConversationFSM:
    """Finite state machine for managing conversation flow."""
    
    def __init__(self, initial_state: ConversationState = ConversationState.SESSION_START):
        self.current_state = initial_state
        self.context: Dict[str, Any] = {
            "consent_granted": False,
            "lesson_id": None,
            "schedule_preference": None,
            "engagement_level": None,
        }
    
    def transition(self, new_state: ConversationState, context_update: Optional[Dict[str, Any]] = None):
        """Transition to a new state."""
        if self.is_valid_transition(self.current_state, new_state):
            self.current_state = new_state
            if context_update:
                self.context.update(context_update)
        else:
            raise ValueError(f"Invalid transition from {self.current_state} to {new_state}")
    
    def is_valid_transition(self, from_state: ConversationState, to_state: ConversationState) -> bool:
        """Check if transition is valid."""
        valid_transitions = {
            ConversationState.SESSION_START: [
                ConversationState.OPT_IN_PROMPT,
                ConversationState.EMERGENCY_FALLBACK,
                ConversationState.END_SESSION
            ],
            ConversationState.OPT_IN_PROMPT: [
                ConversationState.GREETING,
                ConversationState.END_SESSION,
                ConversationState.EMERGENCY_FALLBACK
            ],
            ConversationState.GREETING: [
                ConversationState.TOPIC_INTRO,
                ConversationState.EMERGENCY_FALLBACK,
                ConversationState.END_SESSION
            ],
            ConversationState.TOPIC_INTRO: [
                ConversationState.DELIVER_LESSON_INTRO,
                ConversationState.SAFE_REDIRECT,
                ConversationState.EMERGENCY_FALLBACK,
                ConversationState.END_SESSION
            ],
            ConversationState.DELIVER_LESSON_INTRO: [
                ConversationState.DELIVER_LESSON_BRIEF,
                ConversationState.ENGAGEMENT_CHECK,
                ConversationState.SAFE_REDIRECT,
                ConversationState.EMERGENCY_FALLBACK,
                ConversationState.END_SESSION
            ],
            ConversationState.DELIVER_LESSON_BRIEF: [
                ConversationState.DELIVER_LESSON_DETAILED,
                ConversationState.ENGAGEMENT_CHECK,
                ConversationState.SAFE_REDIRECT,
                ConversationState.EMERGENCY_FALLBACK,
                ConversationState.END_SESSION
            ],
            ConversationState.DELIVER_LESSON_DETAILED: [
                ConversationState.ENGAGEMENT_CHECK,
                ConversationState.SCHEDULE_OFFER,
                ConversationState.SAFE_REDIRECT,
                ConversationState.EMERGENCY_FALLBACK,
                ConversationState.END_SESSION
            ],
            ConversationState.ENGAGEMENT_CHECK: [
                ConversationState.DELIVER_LESSON_DETAILED,
                ConversationState.SCHEDULE_OFFER,
                ConversationState.END_SESSION,
                ConversationState.EMERGENCY_FALLBACK
            ],
            ConversationState.SCHEDULE_OFFER: [
                ConversationState.CONFIRM_SCHEDULE,
                ConversationState.END_SESSION,
                ConversationState.EMERGENCY_FALLBACK
            ],
            ConversationState.CONFIRM_SCHEDULE: [
                ConversationState.END_SESSION,
                ConversationState.EMERGENCY_FALLBACK
            ],
            ConversationState.SAFE_REDIRECT: [
                ConversationState.END_SESSION,
                ConversationState.EMERGENCY_FALLBACK
            ],
            ConversationState.EMERGENCY_FALLBACK: [
                ConversationState.END_SESSION
            ],
            ConversationState.END_SESSION: [],
        }
        return to_state in valid_transitions.get(from_state, [])

