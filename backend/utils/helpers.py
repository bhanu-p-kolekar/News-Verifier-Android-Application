"""
Utility functions for the News Verification API
"""

import re
from typing import Optional
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """
    Check if a string is a valid URL
    
    Args:
        url: String to validate
    
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def clean_text(text: str) -> str:
    """
    Clean and normalize text content
    
    Args:
        text: Raw text to clean
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.,!?;:\-\'"()]', '', text)
    
    return text.strip()


def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL
    
    Args:
        url: URL string
    
    Returns:
        Domain name or None
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Try to truncate at sentence boundary
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > max_length * 0.8:  # If period is in last 20%
        return truncated[:last_period + 1]
    
    return truncated + "..."


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity score between two texts
    Based on word overlap
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)
