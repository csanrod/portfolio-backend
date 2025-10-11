"""This module provides utilities to interact with the vector database."""

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
    """Clean start of the vector database."""
    # Check if collection exists and delete if necessary
    if qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.delete_collection(COLLECTION_NAME)
        logger.info(f"🗑️\tDeleted existing collection: {COLLECTION_NAME}")

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
    logger.info(f"✅\tCollection '{COLLECTION_NAME}' created successfully")

def upsert(ids: list[str], embeddings: list[numpy.ndarray], payloads: list[dict] = None):
    """Insert or update points in the collection.

    Args:
        ids: chunk identifiers (UUID strings).
        embeddings: embeddings for each chunk.
        payloads: (optional) metadata for each chunk.
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
    logger.info("✅\tEmbeddings uploaded successfully")
