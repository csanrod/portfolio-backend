# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Logging System** (`src/portfolio/utils/logger.py`)
  - Centralized logger configuration with standardized formatting
  - Timestamp, module name, and log level in all messages
  - Environment-based log level control via `LOG_LEVEL` env var
  - Automatic module name cleaning (removes "src." prefix, handles `__main__`)

### Changed
- Replaced all `print()` statements with standardized `logger` calls
- Each module now uses `setup_logger(__name__)` for proper traceability
- Log output format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## [0.1.0] - 2025-10-05

### Added
- **Preprocessing Module** (`src/portfolio/intake/preprocessing.py`)
  - `read_markdown_file()`: Reads markdown files with error handling
  - `parse_sections_and_contents()`: O(n) algorithm for hierarchical section parsing (H2/H3)
  - `get_chunks()`: Combines sections with contents into formatted chunks
- **Hierarchical Parsing**: Intelligent H2/H3 relationship detection
  - H2 with H3 subsections → "H2 > H3" paths with H3 content only
  - H2 without H3 → standalone H2 path with all H2 content
- **Comprehensive Documentation**
  - Module-level docstrings for all modules
  - Google-style function docstrings (Args, Returns, Raises, Examples)
  - Full type hints (PEP 484) on all functions
  - Inline comments for complex logic
- **Error Handling**: Robust validation and user-friendly status messages
- **Requirements.txt**: Structured by phases with pinned versions

### Changed
- **README.md**: Minimized to essential information (36 lines, 85% reduction)
- **Main Pipeline**: Three-step workflow (read → parse → chunk)
- Platform-agnostic path handling using `pathlib`

### Fixed
- Cross-platform compatibility (Windows/Linux/macOS) for file paths
- Grammar corrections in output messages ("readed" → "read", "builded" → "built")
- Return type annotations to include `None` cases

### Optimized
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
