"""Main entry point for the portfolio backend application.

This module serves as the application entry point and orchestrates
the RAG pipeline execution.
"""
from pathlib import Path

from .intake import preprocessing as pp
from .utils import setup_logger

logger = setup_logger(__name__)

DOC_PATH = str(Path(__file__).resolve().parents[2] / "docs" / "info_portfolio.md")


def main() -> None:
    """Execute the main RAG preprocessing pipeline.

    This function orchestrates the full preprocessing workflow:
    1. Reads the portfolio markdown document from disk
    2. Parses sections and extracts content for RAG indexing
    3. Builds text chunks combining sections with contents

    The processed chunks are formatted and ready for vectorization
    and storage in the RAG system.

    Returns:
        None
    """
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

    logger.info(f"📊\tProcessed {len(chunks)} chunks successfully.")


if __name__ == "__main__":
    main()