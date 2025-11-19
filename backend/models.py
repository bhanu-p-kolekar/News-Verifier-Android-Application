"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class VerdictType(str, Enum):
    """
    Possible verdict types for news verification
    """
    TRUE = "True"
    FALSE = "False"
    MISLEADING = "Misleading"
    UNVERIFIED = "Unverified"


class VerifyRequest(BaseModel):
    """
    Request model for news verification endpoint
    """
    content: str = Field(
        ...,
        description="News content to verify (can be text or URL)",
        min_length=10,
        max_length=10000
    )
    
    @validator('content')
    def validate_content(cls, v):
        """
        Validate that content is not empty or just whitespace
        """
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "content": "https://example.com/news-article or text content here"
            }
        }


class VerifyResponse(BaseModel):
    """
    Response model for news verification endpoint
    """
    verdict: str = Field(
        ...,
        description="Verification verdict: True, False, Misleading, or Unverified"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence score from 0 to 100"
    )
    summary: str = Field(
        ...,
        description="Brief summary of the verification analysis"
    )
    evidence_links: List[str] = Field(
        default_factory=list,
        description="List of URLs used as evidence"
    )
    
    @validator('verdict')
    def validate_verdict(cls, v):
        """
        Ensure verdict is one of the allowed values
        """
        allowed = ["True", "False", "Misleading", "Unverified"]
        if v not in allowed:
            # Try to match case-insensitively
            for allowed_verdict in allowed:
                if v.lower() == allowed_verdict.lower():
                    return allowed_verdict
            return "Unverified"
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "verdict": "Misleading",
                "confidence": 75,
                "summary": "The claim contains partial truth but lacks important context...",
                "evidence_links": [
                    "https://example.com/source1",
                    "https://example.com/source2"
                ]
            }
        }


class HealthResponse(BaseModel):
    """
    Response model for health check endpoints
    """
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "All services operational"
            }
        }


class NewsArticle(BaseModel):
    """
    Model for news article data
    """
    title: str
    url: str
    source: Optional[str] = None
    snippet: Optional[str] = None
    published_date: Optional[str] = None
