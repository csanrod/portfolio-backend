"""FastAPI application for Portfolio RAG backend.

FastAPI app with health, chat, and intake endpoints.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
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


# Tag descriptions
tags_metadata = [
    {
        "name": "Agent",
        "description": """
**RAG-powered intelligent operations** for portfolio interactions.

These endpoints handle the complete RAG pipeline from data ingestion to query processing:
- **Chat**: Semantic search + LLM-generated responses
- **Intake**: Automated document processing and vectorization
        """,
    },
    {
        "name": "Health",
        "description": """
**System monitoring and health checks** for infrastructure orchestration.

Provides real-time API status information including version and timestamp.
        """,
    },
]

# Create FastAPI application
app = FastAPI(
    title="Portfolio RAG API",
    description="""
## Overview
A **Retrieval-Augmented Generation (RAG)** backend API for portfolio chatbot interactions.

This API combines semantic search with large language models to provide intelligent responses 
about portfolio information.

### Pipeline Architecture
1. **Embeddings**: BGE-M3 model for semantic vector generation
2. **Vector Database**: Qdrant for similarity search
3. **LLM**: GPT-5-nano for natural language generation

### Key Features
- ✅ Real-time chat with portfolio context
- ✅ Automated data ingestion pipeline
- ✅ Sub-10s average response time
- ✅ Health monitoring endpoints
    """,
    version=__version__,
    openapi_tags=tags_metadata,
    docs_url=None,  # Disable Swagger UI
    redoc_url=None,  # Disable ReDoc
    lifespan=lifespan
)

# Register routers (endpoints)
## Agent endpoints
app.include_router(chat_router)
app.include_router(intake_router)

## Health endpoint
app.include_router(health_router)


# Scalar API documentation
@app.get("/", include_in_schema=False)
async def scalar_docs():
    """Serve Scalar API documentation."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        hide_models=True,
    )