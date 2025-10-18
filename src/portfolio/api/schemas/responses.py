"""Response models for API endpoints.

Pydantic schemas for response serialization.
"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(
        ..., 
        description="API health status"
    )
    version: str = Field(
        ..., 
        description="API version"
    )
    timestamp: str = Field(
        ..., 
        description="Timestamp of the response"
    )


class ChatResponse(BaseModel):
    """Chat endpoint response."""
    answer: str = Field(
        ..., 
        description="LLM-generated answer based on portfolio context"
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds"
    )
