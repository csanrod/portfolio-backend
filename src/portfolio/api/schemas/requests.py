"""Request models for API endpoints.

Pydantic schemas for input validation.
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat endpoint request payload."""
    
    user_input: str = Field(
        ..., 
        min_length=1,
        description="User query about the portfolio",
        examples=["What are your hobbies?"]
    )
