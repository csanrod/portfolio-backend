# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Agent Module** (`src/portfolio/agent/agent.py`)
  - Minimal RAG agent with GPT-5-nano reasoning model
  - `build_context()`: Transforms vector search results into structured context
  - `generate_answer()`: Natural language answer generation using OpenAI Responses API
  - Direct OpenAI SDK integration (no LangChain abstraction)
  - Reasoning configuration: `{"effort": "minimal"}` for fast responses
  - Text formatting: `{"verbosity": "low"}` for concise answers
  - Multilingual support: Responds in user's query language, context always in Spanish
  - System prompt with clear instructions for portfolio assistant behavior
  - Fallback answer handling for empty or failed responses
  - 95 lines of pure functional code (no classes)
- **Evaluation Module** (`src/portfolio/evals/ragas.py`)
  - Comprehensive RAGAS integration with 11 quality metrics for RAG tuning
  - **Retrieval Quality** (2 metrics):
    - Context Precision: Ranking quality of retrieved chunks
    - Context Relevance: Pertinence of chunks to query (NVIDIA)
  - **Generation Quality** (3 metrics):
    - Response Relevancy: Answer pertinence to question
    - Faithfulness: No hallucinations vs contexts
    - Response Groundedness: Claims supported by contexts (NVIDIA)
  - **Response Quality - Aspect Critics** (5 metrics with context-optimized definitions):
    - Harmfulness: Offensive/discriminatory/unprofessional content detection (inverted)
    - Maliciousness: Deception/manipulation/exaggeration detection (inverted)
    - Coherence: Logical structure with smooth transitions and no contradictions
    - Correctness: Factual accuracy verifiable against retrieved context
    - Conciseness: Efficient communication without verbosity or redundancy
  - `get_evaluator_llm()`: gpt-5-chat-latest (temperature=0 for determinism, RAGAS-compatible)
  - `get_evaluator_embeddings()`: text-embedding-3-large for maximum precision (3072-dim)
  - Detailed logging with grouped metric display
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
- **Agent Architecture**: Complete refactoring to minimal MVP design
  - Consolidated from 3 files (answer.py, context.py, __init__.py) to 2 files (agent.py, __init__.py)
  - Replaced LangChain abstraction with direct OpenAI SDK (for agent only)
  - Removed `typing.Any` in favor of explicit `dict` types
  - Simplified `build_context()` to single-line list comprehension
  - Removed unnecessary `score` metadata (not used in answer generation)
  - Direct parsing of Responses API output structure
  - Function signatures remain backward-compatible with main.py
- **Main Pipeline** (`src/portfolio/main.py`): Modular architecture with separate functions
  - `intake()`: Complete data ingestion (Preprocessing → Embeddings → Storage)
  - `chat()`: Interactive retrieval loop with semantic search and LLM answer generation
  - `main()`: Entry point with user choice between ingestion and chat
  - Payloads now include chunk text content for retrieval
- **README.md**: Added environment variables section and features list
- **Requirements.txt**: Updated for GPT-5-nano with Responses API
  - Added `openai>=1.59.0` for direct SDK usage
  - Clarified that LangChain is only required for RAGAS evaluation
  - Added descriptive comments for each dependency section
- Platform-agnostic path handling using `pathlib`
- Replaced all `print()` statements with standardized `logger` calls
- Each module now uses `setup_logger(__name__)` for proper traceability
- Log output format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

### Removed
- **Agent Module**: Eliminated redundant files and code
  - Removed `src/portfolio/agent/answer.py` (merged into agent.py)
  - Removed `src/portfolio/agent/context.py` (merged into agent.py)
  - Removed LangChain dependency from agent (kept only for RAGAS)
  - Removed `typing.Any` usage (replaced with explicit `dict`)
  - Removed unused constants (`DEFAULT_MAX_SNIPPETS`, `DEFAULT_SNIPPET_LENGTH`)
  - Removed unnecessary `score` field from chunks (not used in generation)
  - Removed verbose debug logging from context building

### Fixed
- **Responses API Integration**: Corrected parameter structure
  - Fixed `reasoning.summary` requiring organization verification (removed parameter)
  - Fixed `verbosity` parameter placement: moved from root to `text.verbosity`
  - Fixed response parsing: use direct `response.output` iteration instead of `response.content`
  - Fixed text extraction: iterate through `item.content` blocks with `hasattr(block, "text")`
- **ID Generation**: Replaced `hash()` with UUID5 to avoid negative integers (Qdrant requirement)
- **Qdrant API**: Updated from deprecated `recreate_collection()` to `collection_exists()` + `create_collection()`
- **Named Vectors**: Proper vector configuration with `{"dense": embeddings}` format
- Cross-platform compatibility (Windows/Linux/macOS) for file paths
- Grammar corrections in output messages ("readed" → "read", "builded" → "built")
- Return type annotations to include `None` cases

### Optimized
- **Agent Module**: Reduced from ~155 lines (3 files) to 95 lines (1 file)
  - Eliminated intermediate abstraction layers (LangChain wrapper)
  - Direct API calls for better performance and control
  - Removed unused helper functions (`_get_llm`, `_format_context`)
  - List comprehensions instead of verbose loops
  - Single-responsibility functions without over-engineering
- **GPT-5-nano Configuration**: Minimal resource usage
  - `reasoning.effort: "minimal"` for fastest inference
  - `text.verbosity: "low"` for concise responses (fewer tokens)
  - No temperature parameter (fixed by OpenAI for reasoning models)
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
