"""Main entry point for the portfolio RAG backend API.

Launches the FastAPI application with uvicorn.
"""
import uvicorn
from .api import app

def main() -> None:
    """Launch the FastAPI application.
    
    Starts uvicorn server with the FastAPI app.
    Available endpoints:
    - GET  /health  : Health check
    - POST /chat    : RAG-powered chat queries
    - POST /intake  : Data ingestion pipeline
    """
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        timeout_graceful_shutdown=1
    )


if __name__ == "__main__":
    main()
