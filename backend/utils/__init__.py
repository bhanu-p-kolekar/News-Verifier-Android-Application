"""
Utils package initialization
"""

from .helpers import (
    is_valid_url,
    clean_text,
    extract_domain,
    truncate_text,
    calculate_text_similarity
)

__all__ = [
    'is_valid_url',
    'clean_text',
    'extract_domain',
    'truncate_text',
    'calculate_text_similarity'
]
