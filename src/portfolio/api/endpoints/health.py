"""Health check endpoint.

Provides basic health status for monitoring and orchestration.
"""
from datetime import datetime
from fastapi import APIRouter
from ..schemas import HealthResponse
from ...__init__ import __version__

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=200,
    summary="API health check"
)
async def health_check():
    """
    ## Health Check Endpoint
    
    Returns the current health status of the API server.
    
    **Use cases:**
    - Load balancer health checks
    - Kubernetes liveness/readiness probes
    - Monitoring and alerting systems
    - Deployment verification
    
    **Response includes:**
    - `status`: Current API health status (`ok` when operational)
    - `version`: API semantic version
    - `timestamp`: ISO 8601 timestamp of the health check
    
    **Status codes:**
    - `200 OK`: API is healthy and operational
    """
    return HealthResponse(
        status="ok", 
        version=__version__, 
        timestamp=datetime.now().isoformat()
    )
