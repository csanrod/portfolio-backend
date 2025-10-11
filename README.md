# Portfolio Backend

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

RAG-powered backend for an intelligent portfolio chatbot. Processes markdown documents into structured chunks ready for vectorization and semantic search.

## Quick Start

```bash
# Install
git clone https://github.com/csanrod/portfolio-backend.git
cd portfolio-backend
pip install -r requirements.txt

# Configure environment variables
export QDRANT_ENDPOINT="your-qdrant-cluster-url"
export QDRANT_API_KEY="your-qdrant-api-key"
export OPENAI_API_KEY="your-openai-api-key"  # Optional: for RAGAS evaluation

# Run
python -m src.portfolio.main

# Optional: Set log level
LOG_LEVEL=DEBUG python -m src.portfolio.main
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `QDRANT_ENDPOINT` | Yes | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant Cloud API key |
| `OPENAI_API_KEY` | No | OpenAI API key (for RAGAS evaluation) |
| `LOG_LEVEL` | No | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Features

- ✅ **Preprocessing**: Markdown parsing with hierarchical H2/H3 sections
- ✅ **Embeddings**: BGE-M3 model (1024-dim vectors)
- ✅ **Vector Storage**: Qdrant Cloud integration
- ✅ **Semantic Search**: Cosine similarity retrieval (top-k)
- ✅ **Evaluation**: RAGAS metrics (Context Precision, Recall, Faithfulness)
- ✅ **Interactive Mode**: CLI chat interface with real-time search

## Roadmap

- [x] **Phase 1: Preprocessing** - Markdown parsing & chunk creation
- [x] **Phase 2: Vectorization** - Embeddings generation & Qdrant vector DB
- [x] **Phase 3: RAG** - Semantic search & RAGAS evaluation
- [ ] **Phase 4: Deployment** - API & Cloudflare Workers

## License

This project is licensed under the CC BY-NC 4.0 License - see the [LICENSE](LICENSE) file for details.

## Author

**Cristian Sánchez Rodríguez**
- GitHub: [@csanrod](https://github.com/csanrod)
- LinkedIn: [Cristian Sánchez Rodríguez](https://www.linkedin.com/in/csanrod)
