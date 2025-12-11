"""Phone number utilities."""

import re
from typing import Optional


def normalize_phone_number(phone: str) -> Optional[str]:
    """Normalize phone number to E.164 format."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Basic validation
    if len(digits) < 10:
        return None
    
    # Add country code if missing (assuming US +1)
    if len(digits) == 10:
        digits = '1' + digits
    
    return '+' + digits


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    normalized = normalize_phone_number(phone)
    return normalized is not None and len(normalized) >= 12


def format_phone_number(phone: str) -> str:
    """Format phone number for display."""
    normalized = normalize_phone_number(phone)
    if not normalized:
        return phone
    
    # Format as (XXX) XXX-XXXX for US numbers
    if normalized.startswith('+1') and len(normalized) == 12:
        number = normalized[2:]
        return f"({number[:3]}) {number[3:6]}-{number[6:]}"
    
    return normalized

