"""Vector database module for Qdrant Cloud integration.

This module provides utilities to interact with Qdrant Cloud for storing and
retrieving vector embeddings with semantic search capabilities.
"""

import os
import numpy
from qdrant_client import QdrantClient, models
from ..utils import setup_logger

QDRANT_ENDPOINT = os.getenv("QDRANT_ENDPOINT")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "portfolio"

logger = setup_logger(__name__)
qdrant_client = QdrantClient(
    url=QDRANT_ENDPOINT, 
    api_key=QDRANT_API_KEY,
)

def init():
    """Initialize the Qdrant collection with a clean state.
    
    Deletes the existing collection if present and creates a new one with
    named vector configuration for dense embeddings (1024-dim, COSINE distance).
    """
    # Check if collection exists and delete if necessary
    if qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.delete_collection(COLLECTION_NAME)
        logger.debug(f"🗑️\tDeleted existing collection: {COLLECTION_NAME}")

    # Create collection
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "dense": models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE,
            )
        },
    )
    logger.debug(f"✅\tCollection '{COLLECTION_NAME}' created successfully")

def upsert(ids: list[str], embeddings: numpy.ndarray, payloads: list[dict] = None):
    """Insert or update embedding points in the Qdrant collection.

    Args:
        ids: List of UUID strings identifying each chunk.
        embeddings: Numpy array of embeddings with shape (n_chunks, 1024).
        payloads: Optional list of dictionaries containing metadata for each chunk.
    """
    batch_params = {
        "ids": ids,
        "vectors": {"dense": embeddings.tolist()},  # Named vector configuration
    }
    
    if payloads is not None:
        batch_params["payloads"] = payloads
    
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=models.Batch(**batch_params),
    )
    logger.debug("✅\tEmbeddings uploaded successfully")

def search(query_embedding: numpy.ndarray, top_k: int = 3) -> list[dict]:
    """Perform semantic search to find similar chunks.
    
    Searches the Qdrant collection using cosine similarity to find the top-k
    most similar chunks to the query embedding.
    
    Args:
        query_embedding: Query embedding vector with shape (1024,).
        top_k: Number of most similar chunks to retrieve. Defaults to 3.
    
    Returns:
        List of dictionaries, each containing:
            - id (str): Chunk UUID
            - score (float): Cosine similarity score [0, 1]
            - payload (dict): Chunk metadata including text content
    """
    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=("dense", query_embedding.tolist()),
        limit=top_k,
        with_payload=True,
    )
    
    results = []
    for hit in search_result:
        results.append({
            "id": hit.id,
            "score": hit.score,
            "payload": hit.payload if hit.payload else {},
        })
    
    logger.debug(f"🔍\tRetrieved {len(results)} chunks (top-{top_k})")
    return results


