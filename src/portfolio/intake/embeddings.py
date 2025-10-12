"""Embeddings generation module for text vectorization.

This module provides utilities to generate dense vector embeddings from text
chunks using the BGE-M3 model and create deterministic UUIDs for chunk identification.
"""
from ..utils import setup_logger
import numpy
import uuid
from FlagEmbedding import BGEM3FlagModel

logger = setup_logger(__name__)
emb_model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
logger.info("✅\tEmbedding model loaded successfully.")

def get_embeddings(chunks: list[str]) -> list[numpy.ndarray]:
    """Generate dense vector embeddings for text chunks.
    
    Uses the BGE-M3 model with FP16 optimization to generate 1024-dimensional
    dense embeddings suitable for semantic search.

    Args:
        chunks: List of text chunks to embed.

    Returns:
        numpy.ndarray: Array of embeddings with shape (n_chunks, 1024).
    """
    enc = emb_model.encode(
        chunks,
        batch_size=16,
        max_length=1024,
        return_dense=True,
        return_sparse=False,
        return_colbert_vecs=False
    )
    embeddings = enc["dense_vecs"]
    logger.info("✅\tEmbeddings generated successfully")
    return embeddings


def get_ids(chunks: list[str]) -> list[str]:
    """Generate deterministic UUID identifiers for text chunks.
    
    Uses UUID5 (name-based UUID with SHA-1 hashing) to create reproducible
    identifiers based on chunk content. Same content always produces the same ID.

    Args:
        chunks: List of text chunks to generate IDs for.

    Returns:
        List of UUID strings, one for each chunk.
    """
    namespace = uuid.NAMESPACE_DNS
    return [str(uuid.uuid5(namespace, chunk)) for chunk in chunks]
