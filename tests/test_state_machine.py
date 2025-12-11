"""Tests for state machine transitions."""

import pytest
from app.workflows.conversation_fsm import ConversationFSM, ConversationState


def test_valid_state_transitions():
    """Test valid state transitions."""
    fsm = ConversationFSM(ConversationState.SESSION_START)
    
    # Valid transition
    assert fsm.is_valid_transition(ConversationState.SESSION_START, ConversationState.OPT_IN_PROMPT)
    fsm.transition(ConversationState.OPT_IN_PROMPT)
    assert fsm.current_state == ConversationState.OPT_IN_PROMPT
    
    # Another valid transition
    assert fsm.is_valid_transition(ConversationState.OPT_IN_PROMPT, ConversationState.GREETING)
    fsm.transition(ConversationState.GREETING)
    assert fsm.current_state == ConversationState.GREETING


def test_invalid_state_transitions():
    """Test invalid state transitions."""
    fsm = ConversationFSM(ConversationState.SESSION_START)
    
    # Invalid transition
    assert not fsm.is_valid_transition(ConversationState.SESSION_START, ConversationState.END_SESSION)
    
    # Should raise error
    with pytest.raises(ValueError):
        fsm.transition(ConversationState.END_SESSION)


def test_state_context():
    """Test state context updates."""
    fsm = ConversationFSM(ConversationState.SESSION_START)
    
    fsm.transition(
        ConversationState.OPT_IN_PROMPT,
        context_update={"consent_granted": True}
    )
    
    assert fsm.context["consent_granted"] == True


def test_emergency_fallback():
    """Test emergency fallback transitions."""
    fsm = ConversationFSM(ConversationState.DELIVER_LESSON_INTRO)
    
    # Should be able to transition to emergency from any state
    assert fsm.is_valid_transition(ConversationState.DELIVER_LESSON_INTRO, ConversationState.EMERGENCY_FALLBACK)
    fsm.transition(ConversationState.EMERGENCY_FALLBACK)
    assert fsm.current_state == ConversationState.EMERGENCY_FALLBACK
    
    # From emergency, can only go to end session
    assert fsm.is_valid_transition(ConversationState.EMERGENCY_FALLBACK, ConversationState.END_SESSION)
    assert not fsm.is_valid_transition(ConversationState.EMERGENCY_FALLBACK, ConversationState.GREETING)

