# Portfolio Backend

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

RAG-powered backend for an intelligent portfolio chatbot with **GPT-5-nano reasoning model**. Complete pipeline from markdown ingestion to natural language answers using OpenAI Responses API.

## Quick Start

```bash
# Install
git clone https://github.com/csanrod/portfolio-backend.git
cd portfolio-backend
pip install -r requirements.txt

# Configure environment variables
export QDRANT_ENDPOINT="your-qdrant-cluster-url"
export QDRANT_API_KEY="your-qdrant-api-key"
export OPENAI_API_KEY="your-openai-api-key"  # Required: GPT-5-nano agent

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
| `OPENAI_API_KEY` | Yes | OpenAI API key (GPT-5-nano agent + RAGAS evaluation) |
| `LOG_LEVEL` | No | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Features

### RAG Pipeline
- ✅ **Preprocessing**: Markdown parsing with hierarchical H2/H3 sections
- ✅ **Embeddings**: BGE-M3 model (1024-dim vectors)
- ✅ **Vector Storage**: Qdrant Cloud integration
- ✅ **Semantic Search**: Cosine similarity retrieval (top-k)

### LLM Agent
- ✅ **GPT-5-nano**: Reasoning model with minimal effort configuration
- ✅ **Responses API**: Direct OpenAI SDK integration (no LangChain)
- ✅ **Multilingual**: Responds in user's query language (context in Spanish)
- ✅ **Optimized**: Low verbosity for concise, token-efficient answers
- ✅ **Minimal Code**: 95 lines of pure functional Python

### Evaluation & Interface
- ✅ **RAGAS Metrics**: Context Precision, Recall, Faithfulness
- ✅ **Interactive CLI**: Real-time chat with semantic search + LLM answers

## Roadmap

- [x] **Phase 1: Preprocessing** - Markdown parsing & chunk creation
- [x] **Phase 2: Vectorization** - Embeddings generation & Qdrant vector DB
- [x] **Phase 3: RAG** - Semantic search + GPT-5-nano agent + RAGAS evaluation
- [ ] **Phase 4: Deployment** - API & Cloudflare Workers

## License

This project is licensed under the CC BY-NC 4.0 License - see the [LICENSE](LICENSE) file for details.

## Author

**Cristian Sánchez Rodríguez**
- GitHub: [@csanrod](https://github.com/csanrod)
- LinkedIn: [Cristian Sánchez Rodríguez](https://www.linkedin.com/in/csanrod)
