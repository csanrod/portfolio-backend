"""Chat endpoint for RAG-powered queries.

Main endpoint that processes user queries through the RAG pipeline.
"""
import time
from fastapi import APIRouter, HTTPException
from ..schemas import ChatRequest, ChatResponse, ErrorResponse, ValidationErrorResponse
from ...agent import build_context, generate_answer
from ...intake import embeddings as em
from ...storage import vector_db as db
from ...utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter(tags=["Agent"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=200,
    summary="RAG-powered chat query",
    responses={
        422: {
            "model": ValidationErrorResponse,
            "description": "Validation error - Invalid request body (missing or empty `user_input`)",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error - RAG pipeline failure (embedding generation, Qdrant connection, LLM API error, or context building failure)",
        }
    }
)
async def chat(request: ChatRequest):
    """
    ## RAG-Powered Chat Endpoint
    
    Processes natural language queries about portfolio information using a complete RAG pipeline.
    
    ### Pipeline Workflow
    
    1. **Embedding Generation** → Query vectorization using BGE-M3
    2. **Semantic Search** → Similarity search in Qdrant (top-5 most relevant chunks)
    3. **Context Building** → Aggregate retrieved chunks into coherent context
    4. **LLM Generation** → GPT-5-nano generates natural language response
    
    ### Request Body
    
    ```json
    {
      "user_input": "What are your hobbies?"
    }
    ```
    
    ### Response
    
    - `answer`: Natural language response based on portfolio context
    - `processing_time`: Total pipeline execution time in seconds
    
    ### Performance
    
    - **Average latency**: 2-3 seconds
    - **Timeout**: 30 seconds
    
    ### Status Codes
    
    - `200 OK`: Successfully generated response
    - `422 Unprocessable Entity`: Invalid request body (missing or empty `user_input`)
    - `500 Internal Server Error`: RAG pipeline failure
      - Embedding generation error
      - Qdrant connection/search failure
      - LLM API error (OpenAI timeout/rate limit)
      - Context building failure
    """
    start_time = time.perf_counter()
    
    try:
        # Generate query embedding
        user_embedding = em.get_embeddings([request.user_input])[0]
        
        # Semantic search
        results = db.search(user_embedding, top_k=5)
        
        # Generate answer
        context = build_context(request.user_input, results)
        answer = generate_answer(context)
        
        # Calculate processing time
        processing_time = time.perf_counter() - start_time
        
        logger.info(f"✅ Chat processed in {processing_time:.3f}s: {request.user_input[:50]}...")
        
        return ChatResponse(answer=answer, processing_time=processing_time)
        
    except Exception as e:
        processing_time = time.perf_counter() - start_time
        logger.error(f"⛔ Chat error after {processing_time:.3f}s: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"RAG pipeline error: {str(e)}"
        )
