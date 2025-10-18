"""Health check endpoint.

Provides basic health status for monitoring and orchestration.
"""
from datetime import datetime
from fastapi import APIRouter
from ..schemas import HealthResponse
from ...__init__ import __version__

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="ok", 
        version=__version__, 
        timestamp=datetime.now().isoformat()
    )
