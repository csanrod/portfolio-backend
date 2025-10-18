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


class IntakeResponse(BaseModel):
    """Intake endpoint response."""
    status: str = Field(
        ...,
        description="Intake process status (success or error)"
    )
    message: str = Field(
        ...,
        description="Detailed message about the intake process"
    )
    chunks_processed: int = Field(
        ...,
        description="Number of chunks processed and uploaded"
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds"
    )
