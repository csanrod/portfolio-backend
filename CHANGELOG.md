# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Evaluation Module** (`src/portfolio/evals/ragas.py`)
  - RAGAS integration for RAG pipeline quality assessment
  - `evaluate_retrieval()`: Evaluates context precision, recall, and faithfulness
  - `generate_response()`: Auto-generates LLM responses for evaluation
  - OpenAI GPT-4o-mini integration for evaluation metrics
  - Environment-based configuration (`OPENAI_API_KEY`)
- **Storage Module** (`src/portfolio/storage/vector_db.py`)
  - Qdrant Cloud integration for vector storage
  - `init()`: Initialize/recreate collection with proper cleanup
  - `upsert()`: Insert/update embeddings with UUID-based identifiers and payloads
  - `search()`: Semantic search with top-k retrieval and similarity scores
  - Named vector configuration (`dense`) with COSINE distance
  - Environment-based configuration (`QDRANT_ENDPOINT`, `QDRANT_API_KEY`)
- **Embeddings Module** (`src/portfolio/intake/embeddings.py`)
  - `get_embeddings()`: Generates dense vector embeddings for text chunks
  - `get_ids()`: UUID5-based deterministic ID generation for chunks
  - BGEM3FlagModel integration (BAAI/bge-m3) with FP16 optimization
  - Batch processing support (batch_size=16, max_length=1024)
  - Returns numpy arrays for efficient vector operations
- **Preprocessing Module** (`src/portfolio/intake/preprocessing.py`)
  - `read_markdown_file()`: Reads markdown files with error handling
  - `parse_sections_and_contents()`: O(n) algorithm for hierarchical section parsing (H2/H3)
  - `get_chunks()`: Combines sections with contents into formatted chunks
- **Hierarchical Parsing**: Intelligent H2/H3 relationship detection
  - H2 with H3 subsections → "H2 > H3" paths with H3 content only
  - H2 without H3 → standalone H2 path with all H2 content
- **Logging System** (`src/portfolio/utils/logger.py`)
  - Centralized logger configuration with standardized formatting
  - Timestamp, module name, and log level in all messages
  - Environment-based log level control via `LOG_LEVEL` env var
  - Automatic module name cleaning (removes "src." prefix, handles `__main__`)
- **Comprehensive Documentation**
  - Module-level docstrings for all modules
  - Google-style function docstrings (Args, Returns, Raises, Examples)
  - Full type hints (PEP 484) on all functions
  - Inline comments for complex logic
- **Error Handling**: Robust validation and user-friendly status messages
- **Requirements.txt**: Structured by phases with pinned versions

### Changed
- **Main Pipeline** (`src/portfolio/main.py`): Modular architecture with separate functions
  - `intake()`: Complete data ingestion (Preprocessing → Embeddings → Storage)
  - `chat()`: Interactive retrieval loop with semantic search
  - `main()`: Entry point with user choice between ingestion and chat
  - Payloads now include chunk text content for retrieval
- **README.md**: Added environment variables section and features list
- **Requirements.txt**: Updated versions and added RAGAS dependencies
- Platform-agnostic path handling using `pathlib`
- Replaced all `print()` statements with standardized `logger` calls
- Each module now uses `setup_logger(__name__)` for proper traceability
- Log output format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

### Fixed
- **ID Generation**: Replaced `hash()` with UUID5 to avoid negative integers (Qdrant requirement)
- **Qdrant API**: Updated from deprecated `recreate_collection()` to `collection_exists()` + `create_collection()`
- **Named Vectors**: Proper vector configuration with `{"dense": embeddings}` format
- Cross-platform compatibility (Windows/Linux/macOS) for file paths
- Grammar corrections in output messages ("readed" → "read", "builded" → "built")
- Return type annotations to include `None` cases

### Optimized
- Disabled Hugging Face progress bars (`HF_HUB_DISABLE_PROGRESS_BARS=1`) for cleaner output
- Vector dimension: 1024 (truncated from BGE-M3's 8192 for cost/speed optimization)
- Two-phase parsing algorithm with true O(n) complexity
- Pre-compiled regex patterns to avoid recompilation
- Single-pass line classification for efficiency

## [0.0.0] - 2025-10-05

### Added
- Initial project structure with git-flow workflow
- Python package setup with `src/portfolio/`
- Documentation directory for RAG ingestion data
- Standard project files (.gitignore, LICENSE, README, CHANGELOG)
- CC BY-NC 4.0 license
