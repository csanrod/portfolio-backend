"""Intake endpoint for data ingestion.

Endpoint that executes the complete RAG data ingestion pipeline.
"""
import time
from pathlib import Path
from fastapi import APIRouter, HTTPException
from ..schemas import ErrorResponse, IntakeResponse
from ...intake import preprocessing as pp
from ...intake import embeddings as em
from ...storage import vector_db as db
from ...utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter(tags=["Agent"])

DOC_PATH = str(Path(__file__).resolve().parents[4] / "docs" / "info_portfolio.md")


@router.post(
    "/intake",
    response_model=IntakeResponse,
    status_code=200,
    summary="Execute data ingestion pipeline",
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - Pipeline failure (file read error, parsing error, chunking error, embedding generation error, or Qdrant upload error)",
        }
    }
)
async def intake():
    """
    ## Data Ingestion Pipeline
    
    Executes the complete RAG data ingestion workflow to process and vectorize portfolio documents.
    
    ### Pipeline Workflow
    
    1. **Document Preprocessing** → Read and parse markdown file (`info_portfolio.md`)
    2. **Chunking** → Split document into semantic chunks by sections
    3. **Embedding Generation** → Generate BGE-M3 embeddings for each chunk
    4. **Vector Storage** → Upload embeddings and metadata to Qdrant
    
    ### What Gets Processed
    
    - **Source**: `docs/info_portfolio.md`
    - **Chunk Strategy**: Section-based splitting
    - **Vector Dimension**: 1024 (BGE-M3)
    
    ### Response
    
    - `status`: Ingestion status (`success` or `error`)
    - `message`: Detailed operation summary
    - `chunks_processed`: Total number of chunks vectorized and uploaded
    - `processing_time`: Total pipeline execution time in seconds
    
    ### Use Cases
    
    - Initial database population
    - Portfolio content updates
    - Database reset and reingestion
    - CI/CD deployment hooks
    
    ### Performance
    
    - **Typical duration**: 10-20 seconds (depends on document size)
    - **Expected chunks**: ~30-50 chunks
    
    ### Status Codes
    
    - `200 OK`: Ingestion completed successfully
    - `500 Internal Server Error`: Pipeline failure
      - File read error (markdown file not found or corrupted)
      - Parsing error (invalid markdown structure)
      - Chunking error (failed to split document)
      - Embedding generation error (BGE-M3 model failure)
      - Qdrant upload error (connection failure, authentication error, or storage quota exceeded)
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
