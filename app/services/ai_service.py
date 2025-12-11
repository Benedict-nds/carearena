"""AI/LLM service with Whisper ASR, GPT-4o/LLaMA LLM, and TTS."""

import time
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models.safety import AIResponseLog
from app.db.models.conversation import ConversationSession
from app.workflows.conversation_fsm import ConversationState


class AIService:
    """Service for AI/LLM operations with token counting and latency logging."""
    
    def __init__(self, db: Session):
        self.db = db
        self.openai_api_key = settings.OPENAI_API_KEY
        # Model configuration
        self.asr_model = "whisper-1"  # OpenAI Whisper
        self.llm_model = "gpt-4o"  # Can be switched to llama-3 or other models
        self.tts_model = "tts-1"  # OpenAI TTS (African-accent voice)
        self.tts_voice = "alloy"  # Can be configured for African accents
    
    async def transcribe_audio(self, audio_url: str) -> str:
        """Transcribe audio to text using Whisper ASR."""
        start_time = time.time()
        
        try:
            # TODO: Integrate with OpenAI Whisper API
            # import openai
            # openai.api_key = self.openai_api_key
            # with open(audio_url, "rb") as audio_file:
            #     transcript = openai.Audio.transcribe(self.asr_model, audio_file)
            #     return transcript["text"]
            
            # Placeholder implementation
            latency_ms = (time.time() - start_time) * 1000
            print(f"ASR transcription completed in {latency_ms:.2f}ms")
            return "Transcribed text placeholder"
        except Exception as e:
            print(f"ASR error: {e}")
            return ""
    
    async def generate_response(
        self,
        user_input: str,
        current_state: ConversationState,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Generate AI response using GPT-4o or LLaMA."""
        start_time = time.time()
        
        # Build prompt based on current state and context
        prompt = self._build_prompt(user_input, current_state, context, history)
        
        try:
            # TODO: Integrate with OpenAI GPT-4o or LLaMA
            # import openai
            # openai.api_key = self.openai_api_key
            # response = openai.ChatCompletion.create(
            #     model=self.llm_model,
            #     messages=[
            #         {"role": "system", "content": self._get_system_prompt(current_state)},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.7,
            #     max_tokens=500
            # )
            # 
            # response_text = response.choices[0].message.content
            # input_tokens = response.usage.prompt_tokens
            # output_tokens = response.usage.completion_tokens
            # total_tokens = response.usage.total_tokens
            
            # Placeholder implementation
            response_text = f"AI response for state {current_state.value}: {user_input}"
            input_tokens = len(prompt.split())  # Approximate
            output_tokens = len(response_text.split())  # Approximate
            total_tokens = input_tokens + output_tokens
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Log AI response
            self._log_ai_response(
                prompt=prompt,
                response=response_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                latency_ms=latency_ms,
                model_name=self.llm_model
            )
            
            return response_text
        except Exception as e:
            print(f"LLM error: {e}")
            return "I apologize, I'm having trouble processing that. Could you please repeat?"
    
    async def synthesize_speech(self, text: str, language: str = "en") -> str:
        """Synthesize speech from text using TTS (African-accent voice)."""
        start_time = time.time()
        
        try:
            # TODO: Integrate with OpenAI TTS or other TTS service
            # import openai
            # openai.api_key = self.openai_api_key
            # response = openai.Audio.speech.create(
            #     model=self.tts_model,
            #     voice=self.tts_voice,  # Configure for African accent
            #     input=text,
            #     language=language
            # )
            # 
            # # Save audio file
            # audio_url = f"audio/{datetime.utcnow().timestamp()}.mp3"
            # with open(audio_url, "wb") as f:
            #     f.write(response.content)
            # return audio_url
            
            # Placeholder implementation
            latency_ms = (time.time() - start_time) * 1000
            print(f"TTS synthesis completed in {latency_ms:.2f}ms")
            return f"audio/{datetime.utcnow().timestamp()}.mp3"
        except Exception as e:
            print(f"TTS error: {e}")
            return ""
    
    def _build_prompt(
        self,
        user_input: str,
        current_state: ConversationState,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Build prompt for LLM based on current state."""
        state_prompts = {
            ConversationState.OPT_IN_PROMPT: "Ask the patient if they consent to receive health education.",
            ConversationState.GREETING: "Greet the patient warmly and introduce CareArena.",
            ConversationState.TOPIC_INTRO: "Introduce the topic of preeclampsia education.",
            ConversationState.DELIVER_LESSON_INTRO: "Deliver a brief introduction to the lesson.",
            ConversationState.DELIVER_LESSON_BRIEF: "Deliver a brief summary of the lesson content.",
            ConversationState.DELIVER_LESSON_DETAILED: "Deliver detailed lesson content about preeclampsia.",
            ConversationState.ENGAGEMENT_CHECK: "Check if the patient wants to continue learning.",
            ConversationState.SCHEDULE_OFFER: "Offer to schedule future lessons.",
            ConversationState.CONFIRM_SCHEDULE: "Confirm the schedule preference with the patient.",
        }
        
        base_prompt = state_prompts.get(current_state, "Continue the conversation naturally.")
        
        # Add context
        if context.get("lesson_id"):
            base_prompt += f"\nCurrent lesson ID: {context['lesson_id']}"
        
        # Add conversation history
        if history:
            base_prompt += "\n\nConversation history:"
            for msg in history[-3:]:  # Last 3 messages
                base_prompt += f"\n{msg['role']}: {msg['content']}"
        
        base_prompt += f"\n\nUser input: {user_input}"
        base_prompt += "\n\nGenerate a natural, conversational response. Do NOT provide medical diagnosis or advice."
        
        return base_prompt
    
    def _get_system_prompt(self, current_state: ConversationState) -> str:
        """Get system prompt for LLM."""
        return """You are a helpful health education assistant for CareArena, specializing in preeclampsia education.

CRITICAL RULES:
1. You CANNOT diagnose medical conditions
2. You CANNOT provide medical advice
3. You CANNOT prescribe medications
4. If the patient mentions symptoms, redirect them to consult a healthcare provider
5. If there's an emergency, escalate immediately
6. Only deliver pre-approved educational content
7. Be conversational, empathetic, and culturally sensitive
8. Support multiple languages: English, Twi, Ga, Ewe

Your role is to educate, not to diagnose or treat."""
    
    def _log_ai_response(
        self,
        prompt: str,
        response: str,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
        latency_ms: float,
        model_name: str,
        session_id: Optional[int] = None,
        turn_id: Optional[int] = None
    ):
        """Log AI response for audit purposes."""
        log = AIResponseLog(
            session_id=session_id,
            turn_id=turn_id,
            model_name=model_name,
            prompt=prompt,
            response=response,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms,
            created_at=datetime.utcnow()
        )
        self.db.add(log)
        self.db.commit()
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text (approximate)."""
        # Simple approximation: ~4 characters per token
        # TODO: Use tiktoken library for accurate counting
        return len(text) // 4

