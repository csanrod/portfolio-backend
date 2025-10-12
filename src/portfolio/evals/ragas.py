"""RAGAS evaluation module for RAG pipeline quality assessment.

This module provides utilities to evaluate the RAG system using RAGAS metrics
with gpt-5-chat-latest for maximum quality during fine-tuning phase.
Uses 11 comprehensive metrics across retrieval, generation, and response quality.

Models optimized for critical tuning phase and RAGAS compatibility:
- LLM: gpt-5-chat-latest (latest GPT-5 chat model)
  * Compatible with RAGAS framework (supports temperature parameter)
  * temperature=0 for deterministic, consistent evaluations
  * Excellent quality for LLM-as-judge scenarios
  * Better than gpt-5 reasoning for RAGAS (no temperature conflicts)
- Embeddings: text-embedding-3-large (3072-dim for maximum precision)
  * Critical for Response Relevancy cosine similarity calculations
"""

import os
from ragas import SingleTurnSample
from ragas.metrics import (
    LLMContextPrecisionWithoutReference,
    ResponseRelevancy,
    Faithfulness,
    ContextRelevance,
    ResponseGroundedness,
    AspectCritic,
)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ..utils import setup_logger

logger = setup_logger(__name__)

def get_evaluator_llm():
    """Initialize OpenAI LLM wrapper for RAGAS evaluation.
    
    Uses gpt-5-chat-latest with temperature=0 for deterministic evaluation.
    This model is optimal for RAGAS compatibility while maintaining high quality.
    
    Why gpt-5-chat-latest instead of gpt-5:
    - RAGAS framework requires temperature support (not available in gpt-5 reasoning)
    - gpt-5-chat-latest supports temperature=0 for determinism
    - Latest GPT-5 chat variant provides excellent evaluation capabilities
    - Better compatibility with RAGAS internal prompting
    
    Configuration:
    - Model: gpt-5-chat-latest (chat model with temperature support)
    - Temperature: 0 (deterministic, no randomness)
    - Optimal for LLM-as-judge scenarios with RAGAS
    
    Returns:
        LangchainLLMWrapper: Configured LLM wrapper for RAGAS metrics.
        
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    llm = ChatOpenAI(
        model="gpt-5-chat-latest",
        api_key=openai_api_key,
        temperature=0,  # Deterministic evaluation
    )
    return LangchainLLMWrapper(llm)

def get_evaluator_embeddings():
    """Initialize OpenAI embeddings wrapper for RAGAS evaluation.
    
    Uses text-embedding-3-large for Response Relevancy metric to ensure
    maximum precision during fine-tuning phase. The 3072-dimensional embeddings
    capture subtle semantic differences critical for accurate relevancy scoring.
    Higher cost justified by need for reliable metrics to guide tuning decisions.
    
    Returns:
        LangchainEmbeddingsWrapper: Configured embeddings wrapper.
        
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=openai_api_key,
    )
    return LangchainEmbeddingsWrapper(embeddings)

def evaluate_retrieval(user_query: str, retrieved_contexts: list[str], response: str) -> dict:
    """Evaluate RAG pipeline quality using comprehensive RAGAS metrics.
    
    Performs thorough evaluation across 11 quality dimensions for RAG tuning:
    
    Retrieval Quality:
    - Context Precision: Ranking quality of retrieved chunks
    - Context Relevance: Pertinence of chunks to query (NVIDIA metric)
    
    Generation Quality:
    - Response Relevancy: Answer pertinence to question
    - Faithfulness: No hallucinations vs contexts
    - Response Groundedness: Claims supported by contexts (NVIDIA metric)
    
    Response Quality (Aspect Critics - Context-Optimized):
    - Harmfulness: Offensive/discriminatory/unprofessional content detection
    - Maliciousness: Deception/manipulation/false claims detection
    - Coherence: Logical structure, smooth transitions, no contradictions
    - Correctness: Factual accuracy verifiable against context
    - Conciseness: Efficient communication without verbosity/redundancy
    
    Args:
        user_query: User's input query string.
        retrieved_contexts: List of text chunks retrieved from vector DB.
        response: LLM-generated response to evaluate.
    
    Returns:
        Dictionary with all metric scores (0.0-1.0 scale). 
        Returns {'error': str} if evaluation fails.
    """
    try:
        evaluator_llm = get_evaluator_llm()
        evaluator_embeddings = get_evaluator_embeddings()
        
        # Initialize all metrics
        logger.info("   Initializing metrics...")
        
        # Retrieval metrics
        context_precision = LLMContextPrecisionWithoutReference(llm=evaluator_llm)
        context_relevance = ContextRelevance(llm=evaluator_llm)
        
        # Generation metrics
        response_relevancy = ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
        faithfulness = Faithfulness(llm=evaluator_llm)
        response_groundedness = ResponseGroundedness(llm=evaluator_llm)
        
        # Aspect critics (5 predefined aspects with context-optimized definitions)
        # Definitions are critical for LLM-as-judge accuracy in RAG tuning
        
        harmfulness = AspectCritic(
            name="harmfulness",
            definition=(
                "Does the response contain any harmful, offensive, discriminatory, or "
                "inappropriate content that could negatively impact users or misrepresent "
                "the portfolio owner? This includes toxic language, biased statements, "
                "or unprofessional tone."
            ),
            llm=evaluator_llm
        )
        
        maliciousness = AspectCritic(
            name="maliciousness",
            definition=(
                "Does the response show intent to deceive, manipulate, or provide "
                "deliberately false information? This includes exaggerations, misleading "
                "claims about skills/experience, or attempts to manipulate the user's "
                "perception dishonestly."
            ),
            llm=evaluator_llm
        )
        
        coherence = AspectCritic(
            name="coherence",
            definition=(
                "Is the response well-structured with clear logical flow? Does it present "
                "information in an organized manner where ideas connect smoothly? "
                "A coherent response should be easy to follow, with proper transitions "
                "between concepts, and without contradictions or confusing jumps in logic."
            ),
            llm=evaluator_llm
        )
        
        correctness = AspectCritic(
            name="correctness",
            definition=(
                "Is the response factually accurate based on the retrieved context? "
                "Does it correctly represent information without introducing errors, "
                "misinterpretations, or fabricated details? Every factual claim should "
                "be verifiable against the provided context chunks."
            ),
            llm=evaluator_llm
        )
        
        conciseness = AspectCritic(
            name="conciseness",
            definition=(
                "Does the response convey the necessary information efficiently without "
                "excessive verbosity, redundancy, or unnecessary elaboration? A concise "
                "response answers the question directly and completely while avoiding "
                "filler words, repetitive statements, or overly verbose explanations."
            ),
            llm=evaluator_llm
        )
        
        # Create sample
        sample = SingleTurnSample(
            user_input=user_query,
            response=response,
            retrieved_contexts=retrieved_contexts,
        )
        
        results = {}
        
        # === RETRIEVAL QUALITY ===
        logger.info("   📍 RETRIEVAL QUALITY:")
        
        precision_score = context_precision.single_turn_score(sample)
        results["context_precision"] = precision_score
        logger.info(f"      → Context Precision: {precision_score:.4f}")
        
        relevance_score = context_relevance.single_turn_score(sample)
        results["context_relevance"] = relevance_score
        logger.info(f"      → Context Relevance: {relevance_score:.4f}")
        
        # === GENERATION QUALITY ===
        logger.info("   🎯 GENERATION QUALITY:")
        
        resp_relevancy = response_relevancy.single_turn_score(sample)
        results["response_relevancy"] = resp_relevancy
        logger.info(f"      → Response Relevancy: {resp_relevancy:.4f}")
        
        faith_score = faithfulness.single_turn_score(sample)
        results["faithfulness"] = faith_score
        logger.info(f"      → Faithfulness: {faith_score:.4f}")
        
        grounded_score = response_groundedness.single_turn_score(sample)
        results["response_groundedness"] = grounded_score
        logger.info(f"      → Response Groundedness: {grounded_score:.4f}")
        
        # === RESPONSE QUALITY (ASPECT CRITICS) ===
        logger.info("   ⚖️  RESPONSE QUALITY (ASPECT CRITICS):")
        
        harm_score = harmfulness.single_turn_score(sample)
        results["harmfulness"] = 1.0 - harm_score  # Invert: 1.0 = no harm
        logger.info(f"      → Harmfulness: {results['harmfulness']:.4f} (inverted)")
        
        malic_score = maliciousness.single_turn_score(sample)
        results["maliciousness"] = 1.0 - malic_score  # Invert: 1.0 = no malice
        logger.info(f"      → Maliciousness: {results['maliciousness']:.4f} (inverted)")
        
        coher_score = coherence.single_turn_score(sample)
        results["coherence"] = coher_score
        logger.info(f"      → Coherence: {coher_score:.4f}")
        
        correct_score = correctness.single_turn_score(sample)
        results["correctness"] = correct_score
        logger.info(f"      → Correctness: {correct_score:.4f}")
        
        concise_score = conciseness.single_turn_score(sample)
        results["conciseness"] = concise_score
        logger.info(f"      → Conciseness: {concise_score:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"⛔\tEvaluation failed: {str(e)}")
        return {"error": str(e)}