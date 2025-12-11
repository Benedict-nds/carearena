"""Language utilities."""

from typing import Dict, List


SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ar": "Arabic",
}


def is_supported_language(language_code: str) -> bool:
    """Check if language code is supported."""
    return language_code.lower() in SUPPORTED_LANGUAGES


def get_language_name(language_code: str) -> str:
    """Get language name from code."""
    return SUPPORTED_LANGUAGES.get(language_code.lower(), "Unknown")


def get_supported_languages() -> List[Dict[str, str]]:
    """Get list of supported languages."""
    return [
        {"code": code, "name": name}
        for code, name in SUPPORTED_LANGUAGES.items()
    ]


def detect_language(text: str) -> str:
    """Detect language from text (simplified)."""
    # TODO: Implement proper language detection
    # For now, return default
    return "en"

