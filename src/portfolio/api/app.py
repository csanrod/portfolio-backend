"""FastAPI application for Portfolio RAG backend.

Minimal API with health check endpoint.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from ..utils import setup_logger
from ..__init__ import __version__
from .endpoints import health_router

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.
    
    Handles startup and shutdown logic.
    """
    # Startup
    logger.info("🚀 Portfolio RAG API started")
    yield
    # Shutdown
    logger.info("🛑 Portfolio RAG API stopped")


# Create FastAPI application
app = FastAPI(
    title="Portfolio RAG API",
    description="Minimal RAG-powered chatbot API",
    version=__version__,
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

# Register routers (endpoints)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8001,
        timeout_graceful_shutdown=1
    )