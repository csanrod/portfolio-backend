"""FastAPI application for Portfolio RAG backend.

FastAPI app with health, chat, and intake endpoints.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..utils import setup_logger
from ..__init__ import __version__
from .endpoints import chat_router, health_router, intake_router

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
app.include_router(chat_router)
app.include_router(intake_router)