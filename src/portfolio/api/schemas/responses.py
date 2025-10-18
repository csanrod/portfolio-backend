"""Response models for API endpoints.

Pydantic schemas for response serialization.
"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="API health status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Timestamp of the response")
