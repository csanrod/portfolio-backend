"""RAGAS evaluation module for RAG pipeline quality assessment.

This module provides utilities to evaluate the RAG system using RAGAS metrics.
"""

import os
from ragas import SingleTurnSample, evaluate
from ragas.metrics import LLMContextPrecisionWithoutReference, ContextRecall, Faithfulness
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ..utils import setup_logger

logger = setup_logger(__name__)

def get_evaluator_llm():
    """Initialize OpenAI LLM wrapper for RAGAS evaluation.
    
    Creates a LangchainLLMWrapper instance with GPT-4o-mini configured for
    deterministic evaluation (temperature=0).
    
    Returns:
        LangchainLLMWrapper: Configured LLM wrapper for RAGAS metrics.
        
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openai_api_key,
        temperature=0,
    )
    return LangchainLLMWrapper(llm)

def evaluate_retrieval(user_query: str, retrieved_contexts: list[str], response: str = None, reference: str = None) -> dict:
    """Evaluate RAG retrieval quality using RAGAS metrics.
    
    Computes multiple quality metrics for the retrieved contexts:
    - Context Precision: Relevance of retrieved contexts to the query
    - Context Recall: Coverage of reference information (if provided)
    - Faithfulness: Alignment of response with retrieved contexts (if provided)
    
    Args:
        user_query: User's input query string.
        retrieved_contexts: List of text chunks retrieved from vector DB.
        response: Optional LLM-generated response for faithfulness evaluation.
        reference: Optional ground truth answer for recall evaluation.
    
    Returns:
        Dictionary containing metric scores. Always includes 'context_precision'.
        May include 'context_recall' and 'faithfulness' if inputs are provided.
        Returns {'error': str} if evaluation fails.
    """
    try:
        evaluator_llm = get_evaluator_llm()
        
        # Initialize metrics
        context_precision = LLMContextPrecisionWithoutReference(llm=evaluator_llm)
        context_recall = ContextRecall(llm=evaluator_llm)
        faithfulness = Faithfulness(llm=evaluator_llm)
        
        # Create sample
        sample = SingleTurnSample(
            user_input=user_query,
            response=response or "No response generated",
            retrieved_contexts=retrieved_contexts,
            reference=reference,
        )
        
        # Evaluate metrics
        results = {}
        
        # Context Precision (how relevant are retrieved contexts)
        precision_score = context_precision.single_turn_score(sample)
        results["context_precision"] = precision_score
        logger.info(f"📊\tContext Precision: {precision_score:.4f}")
        
        # Context Recall (if reference is provided)
        if reference:
            recall_score = context_recall.single_turn_score(sample)
            results["context_recall"] = recall_score
            logger.info(f"📊\tContext Recall: {recall_score:.4f}")
        
        # Faithfulness (if response is provided)
        if response:
            faithfulness_score = faithfulness.single_turn_score(sample)
            results["faithfulness"] = faithfulness_score
            logger.info(f"📊\tFaithfulness: {faithfulness_score:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"⛔\tEvaluation failed: {str(e)}")
        return {"error": str(e)}