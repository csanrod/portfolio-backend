"""Main entry point for the portfolio RAG backend application.

This module orchestrates the complete RAG pipeline, providing an interactive
CLI interface to choose between data ingestion and semantic search chat modes.
"""
from pathlib import Path

from .intake import preprocessing as pp
from .intake import embeddings as em
from .utils import setup_logger
from .storage import vector_db as db
from .evals import ragas

logger = setup_logger(__name__)

DOC_PATH = str(Path(__file__).resolve().parents[2] / "docs" / "info_portfolio.md")


def intake(): 
    """Execute the RAG data ingestion pipeline.

    This function orchestrates the complete data ingestion workflow:
    1. Preprocessing: Reads and parses the markdown document into chunks
    2. Embeddings: Generates vector embeddings for each chunk
    3. Storage: Uploads chunks with embeddings to Qdrant vector database

    Returns:
        None
    """
    # Preprocessing
    md = pp.read_markdown_file(DOC_PATH)
    if md is None:
        logger.error("⛔\tFailed to read markdown file. Exiting.")
        return

    sections, contents = pp.parse_sections_and_contents(md)
    if sections is None or contents is None:
        logger.error("⛔\tFailed to parse sections. Exiting.")
        return

    chunks = pp.get_chunks(sections, contents)
    if chunks is None:
        logger.error("⛔\tFailed to get chunks. Exiting.")
        return

    # Embeddings
    embeddings = em.get_embeddings(chunks)
    ids = em.get_ids(chunks)
    
    # Prepare payloads with chunk content
    payloads = [{"text": chunk} for chunk in chunks]

    # Storage
    db.init()
    db.upsert(ids, embeddings, payloads)


def chat():
    """Execute the RAG retrieval pipeline in interactive mode.

    This function implements a continuous chat loop that:
    1. Accepts user queries via terminal input
    2. Generates embedding vectors for each query
    3. Performs semantic search in Qdrant to retrieve top-k similar chunks
    4. Displays retrieved chunks with similarity scores

    Type 'q' to exit the chat.

    Returns:
        None
    """
    while True:
        logger.info("Press q to quit.")
        user_input = input("> ")
        if user_input == "q":
            logger.info("Bye!")
            break

        # Generate embedding for user query
        user_embedding = em.get_embeddings([user_input])[0]
        
        # Search for similar chunks
        results = db.search(user_embedding, top_k=5)
        
        # Evaluate retrieval
        # ragas.evaluate_retrieval(user_input, [result['payload'].get('text', 'N/A') for result in results])
        
        # Display retrieved chunks
        for i, result in enumerate(results, 1):
            logger.info(f"📄 Chunk {i} (Score: {result['score']:.4f}):")
            logger.info(f"{result['payload'].get('text', 'N/A')}\n")


def main() -> None:
    """Entry point for the portfolio RAG application.

    Provides an interactive interface to choose between:
    - Data ingestion: Processes and uploads portfolio data to vector DB
    - Chat mode: Interactive retrieval of portfolio information via queries

    The chat mode is always available after the initial prompt.

    Returns:
        None
    """
    while True:
        user_input = input("Do you want to intake the portfolio? (y/n): ")
        if user_input == "y" or user_input == "n":
            break
        else:
            logger.warning("⛔\tInvalid input. Please enter 'y' or 'n'.")

    if user_input == "y":        
        intake()

    chat()
            

if __name__ == "__main__":
    main()