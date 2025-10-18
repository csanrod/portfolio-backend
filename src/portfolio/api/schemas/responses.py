"""Response models for API endpoints.

Pydantic schemas for response serialization.
"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(
        ..., 
        description="API health status",
        examples=["ok"]
    )
    version: str = Field(
        ..., 
        description="API version",
        examples=["1.0.0"]
    )
    timestamp: str = Field(
        ..., 
        description="Timestamp of the response",
        examples=["2025-10-18T12:07:00.123456"]
    )


class ChatResponse(BaseModel):
    """Chat endpoint response."""
    answer: str = Field(
        ..., 
        description="LLM-generated answer based on portfolio context",
        examples=["I enjoy various hobbies including reading, hiking, and photography. In my free time, I particularly love exploring new technologies and contributing to open-source projects."]
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
        examples=[2.345]
    )


class IntakeResponse(BaseModel):
    """Intake endpoint response."""
    status: str = Field(
        ...,
        description="Intake process status (success or error)",
        examples=["success"]
    )
    message: str = Field(
        ...,
        description="Detailed message about the intake process",
        examples=["Successfully processed and uploaded 42 chunks to Qdrant"]
    )
    chunks_processed: int = Field(
        ...,
        description="Number of chunks processed and uploaded",
        examples=[42]
    )
    processing_time: float = Field(
        ...,
        description="Processing time in seconds",
        examples=[15.234]
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(
        ...,
        description="Error message describing what went wrong",
        examples=["RAG pipeline error: Failed to connect to Qdrant"]
    )


class ValidationErrorDetail(BaseModel):
    """Validation error detail."""
    type: str = Field(..., description="Error type", examples=["missing"])
    loc: list[str] = Field(..., description="Location of the error", examples=[["body", "user_input"]])
    msg: str = Field(..., description="Error message", examples=["Field required"])


class ValidationErrorResponse(BaseModel):
    """Validation error response (422)."""
    detail: list[ValidationErrorDetail] = Field(
        ...,
        description="List of validation errors"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": [
                        {
                            "type": "missing",
                            "loc": ["body", "user_input"],
                            "msg": "Field required"
                        }
                    ]
                }
            ]
        }
    }
