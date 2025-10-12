"""LLM agent for portfolio query responses.

Minimal RAG agent using OpenAI GPT-5-nano reasoning model with Responses API.
"""

import os

from openai import OpenAI

from ..utils import setup_logger

logger = setup_logger(__name__)

_SYSTEM_PROMPT = """You are a professional portfolio assistant.

Instructions:
- Answer based ONLY on the provided context (always in Spanish)
- Respond in the SAME LANGUAGE the user uses in their question
- Be concise, accurate, and professional
- If context lacks relevant information, acknowledge it clearly

The context contains text chunks retrieved from a portfolio document."""

_FALLBACK_ANSWER = (
    "No relevant portfolio information was found. "
    "Try rephrasing or update the source document."
)


def build_context(query: str, results: list[dict]) -> dict:
    """Transform vector search results into agent context.

    Args:
        query: User query string.
        results: Search results with 'payload' and 'score' keys.

    Returns:
        Dictionary with 'query' and 'retrieved_chunks' keys.
    """
    chunks = [item.get("payload", {}).get("text", "N/A") for item in results[:5]]
    return {"query": query, "retrieved_chunks": chunks}


def generate_answer(context: dict) -> str:
    """Generate natural language answer using GPT-5-nano reasoning model.

    Uses OpenAI Responses API directly with minimal reasoning and low verbosity.

    Args:
        context: Dictionary with 'query' and 'retrieved_chunks' keys.

    Returns:
        LLM-generated answer string or fallback message on error.
    """
    chunks = context.get("retrieved_chunks", [])
    query = context.get("query", "")

    if not chunks:
        logger.warning("No chunks available for answer generation")
        return _FALLBACK_ANSWER

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        client = OpenAI(api_key=api_key)
        context_text = "\n\n".join(chunks)

        response = client.responses.create(
            model="gpt-5-nano",
            input=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"},
            ],
            reasoning={"effort": "minimal"},
            text={"verbosity": "low"},
        )

        # Extract text from response output
        for item in response.output:
            if item.type == "message":
                text = "".join(
                    block.text for block in item.content 
                    if hasattr(block, "text")
                )
                logger.info("✅\tLLM answer generated successfully")
                return text

        return _FALLBACK_ANSWER

    except Exception as e:
        logger.error(f"⛔\tLLM generation failed: {str(e)}")
        return _FALLBACK_ANSWER
