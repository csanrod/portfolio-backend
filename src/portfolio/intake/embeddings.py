"""This module provides utilities to generate embeddings for text data."""
from ..utils import setup_logger
import numpy
import uuid
from FlagEmbedding import BGEM3FlagModel

logger = setup_logger(__name__)
emb_model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
logger.info("✅\tEmbedding model loaded successfully.")

def get_embeddings(chunks: list[str]) -> list[numpy.ndarray]:
    """
    Generate embeddings for a list of text chunks.

    Args:
        chunks: List of normalized text chunks.

    Returns:
        list[numpy.ndarray]: List of embeddings for each chunk.
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
    """
    Generate unique identifiers for a list of text chunks using UUID5.

    Args:
        chunks: List of normalized text chunks.

    Returns:
        list[str]: List of UUID strings for each chunk.
    """
    # UUID5 generates deterministic UUIDs based on content
    namespace = uuid.NAMESPACE_DNS
    return [str(uuid.uuid5(namespace, chunk)) for chunk in chunks]
