"""Agent package for LLM-powered portfolio query responses.

Minimal RAG agent that transforms vector search results into natural language
answers using OpenAI models.
"""

from .agent import build_context, generate_answer

__all__ = ["build_context", "generate_answer"]
