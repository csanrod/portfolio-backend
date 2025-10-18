"""Intake endpoint for data ingestion.

Endpoint that executes the complete RAG data ingestion pipeline.
"""
import time
from pathlib import Path
from fastapi import APIRouter, HTTPException
from ..schemas import IntakeResponse
from ...intake import preprocessing as pp
from ...intake import embeddings as em
from ...storage import vector_db as db
from ...utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter(tags=["Intake"])

DOC_PATH = str(Path(__file__).resolve().parents[4] / "docs" / "info_portfolio.md")


@router.post("/intake", response_model=IntakeResponse)
async def intake():
    """
    Execute RAG data ingestion pipeline.
    
    This endpoint orchestrates the complete data ingestion workflow:
    1. Preprocessing: Reads and parses markdown document into chunks
    2. Embeddings: Generates vector embeddings for each chunk
    3. Storage: Uploads chunks with embeddings to Qdrant
    
    Returns:
        IntakeResponse with status, message, chunks count, and processing time.
    
    Raises:
        HTTPException: 500 if ingestion pipeline fails.
    """
    start_time = time.perf_counter()
    
    try:
        # Preprocessing
        logger.info("🔄 Starting intake process...")
        
        md = pp.read_markdown_file(DOC_PATH)
        if md is None:
            raise ValueError("Failed to read markdown file")
        
        sections, contents = pp.parse_sections_and_contents(md)
        if sections is None or contents is None:
            raise ValueError("Failed to parse sections")
        
        chunks = pp.get_chunks(sections, contents)
        if chunks is None:
            raise ValueError("Failed to get chunks")
        
        # Embeddings
        embeddings = em.get_embeddings(chunks)
        ids = em.get_ids(chunks)
        
        # Prepare payloads
        payloads = [{"text": chunk} for chunk in chunks]
        
        # Storage
        db.init()
        db.upsert(ids, embeddings, payloads)
        
        # Calculate processing time
        processing_time = time.perf_counter() - start_time
        chunks_count = len(chunks)
        
        logger.info(f"✅ Intake completed in {processing_time:.3f}s: {chunks_count} chunks processed")
        
        return IntakeResponse(
            status="success",
            message=f"Successfully processed and uploaded {chunks_count} chunks to Qdrant",
            chunks_processed=chunks_count,
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.perf_counter() - start_time
        logger.error(f"⛔ Intake error after {processing_time:.3f}s: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Intake pipeline error: {str(e)}"
        )
