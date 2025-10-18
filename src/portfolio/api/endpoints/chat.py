"""Chat endpoint for RAG-powered queries.

Main endpoint that processes user queries through the RAG pipeline.
"""
import time
from fastapi import APIRouter, HTTPException
from ..schemas import ChatRequest, ChatResponse
from ...agent import build_context, generate_answer
from ...intake import embeddings as em
from ...storage import vector_db as db
from ...utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG-powered chat endpoint.
    
    Processes user queries through the complete RAG pipeline:
    1. Generate embedding for user query
    2. Semantic search in Qdrant (top-5 chunks)
    3. Generate answer using GPT-5-nano
    4. Return natural language response with processing time
    
    Args:
        request: Chat request with user_input field.
    
    Returns:
        ChatResponse with LLM-generated answer and processing time.
    
    Raises:
        HTTPException: 500 if RAG pipeline fails.
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
        logger.error(f"⛔ Chat error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="RAG pipeline error"
        )
