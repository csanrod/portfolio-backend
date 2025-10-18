# Portfolio Backend

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)
![RAGAS](https://img.shields.io/badge/RAGAS-0.3.5-ff6b6b.svg)
![Evaluated](https://img.shields.io/badge/RAG-Evaluated-success.svg)

**Production-ready RAG API** for intelligent portfolio chatbot interactions. Complete pipeline from data ingestion to REST endpoints with **GPT-5-nano reasoning model**, comprehensive evaluation metrics, and interactive API documentation.

## Quick Start

```bash
# 1. Install dependencies
git clone https://github.com/csanrod/portfolio-backend.git
cd portfolio-backend
pip install -r requirements.txt

# 2. Configure environment variables
export QDRANT_ENDPOINT="your-qdrant-cluster-url"
export QDRANT_API_KEY="your-qdrant-api-key"
export OPENAI_API_KEY="your-openai-api-key"

# 3. Start API server
python -m src.portfolio.main

# 4. Access endpoints
# - API Documentation: http://localhost:8001/
# - Health Check: http://localhost:8001/health
# - OpenAPI Schema: http://localhost:8001/openapi.json
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `QDRANT_ENDPOINT` | Yes | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Yes | Qdrant Cloud API key |
| `OPENAI_API_KEY` | Yes | OpenAI API key (GPT-5-nano agent + RAGAS evaluation) |
| `LOG_LEVEL` | No | Logging level: `DEBUG` (verbose) or `ERROR` (silent, default) |

## API Endpoints

### **GET** `/health` - Health Check
Returns API health status for monitoring and orchestration.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-10-18T12:07:00.123456"
}
```

### **POST** `/chat` - RAG-Powered Chat
Processes natural language queries through the complete RAG pipeline.

**Request:**
```json
{
  "user_input": "What are your hobbies?"
}
```

**Response:**
```json
{
  "answer": "I enjoy various hobbies including reading, hiking, and photography...",
  "processing_time": 2.345
}
```

**Pipeline:**
1. Query vectorization (BGE-M3)
2. Semantic search in Qdrant
3. Context aggregation
4. LLM generation (GPT-5-nano)

---

**ℹ️ Note:** A private `/intake` endpoint exists for data ingestion and vector database management. This endpoint is restricted and not intended for public use. The system is deployed with pre-loaded portfolio data in Qdrant.

### **Interactive Documentation**

Access the complete interactive API documentation with try-it-out functionality at:
- **Scalar UI**: http://localhost:8001/

## Tech Stack

### **Backend Framework**
- **FastAPI 0.115+**: Modern async Python web framework
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic v2**: Data validation with type hints

### **RAG Components**
- **BGE-M3**: Multilingual embedding model
  - ⚠️ **Current**: Local model loaded in-memory (heavyweight)
  - 🎯 **Roadmap**: Migration to API-based consumption for lightweight cloud deployments
- **Qdrant**: Vector database for similarity search
- **OpenAI GPT-5-nano**: Advanced reasoning model

### **Evaluation**
- **RAGAS 0.3.5**: Comprehensive RAG evaluation metrics
- **LangChain**: Framework for RAGAS integration

### **Documentation**
- **Scalar**: Interactive API documentation UI
- **OpenAPI 3.1**: Automatic schema generation

## Features

### REST API
- ✅ **Public Endpoints**: `/health` (monitoring) and `/chat` (RAG queries)
- ✅ **FastAPI 0.115+**: Modern async framework with automatic OpenAPI generation
- ✅ **Scalar Integration**: Beautiful interactive documentation
- ✅ **Pydantic v2**: Request/response validation with examples
- ✅ **Error Handling**: Comprehensive error responses (422, 500)
- ✅ **Performance Metrics**: Processing time tracking on all endpoints
- ✅ **Health Monitoring**: Kubernetes-ready health checks
- ✅ **CORS Ready**: Prepared for frontend integration

### RAG Pipeline
- ✅ **Preprocessing**: Markdown parsing with hierarchical H2/H3 sections
- ✅ **Embeddings**: BGE-M3 model (local in-memory)
- ✅ **Vector Storage**: Qdrant Cloud integration (pre-loaded data)
- ✅ **Semantic Search**: Cosine similarity retrieval

### LLM Agent
- ✅ **GPT-5-nano**: Reasoning model with minimal effort configuration
- ✅ **Responses API**: Direct OpenAI SDK integration
- ✅ **Multilingual**: Responds in user's query language
- ✅ **Optimized**: Low verbosity for concise, token-efficient answers

### Evaluation
- ✅ **RAGAS Metrics**: 11 comprehensive metrics for RAG fine-tuning
  - **Models**: gpt-5-chat-latest (temperature=0) + text-embedding-3-large (3072-dim)
  - **Retrieval Quality**: Context Precision, Context Relevance
  - **Generation Quality**: Response Relevancy, Faithfulness, Groundedness
  - **Response Quality**: Harmfulness, Maliciousness, Coherence, Correctness, Conciseness

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Frontend)                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│         ┌──────────────┐       ┌──────────────┐            │
│         │   /health    │       │    /chat     │            │
│         └──────┬───────┘       └──────┬───────┘            │
│                │                       │                     │
│                ▼                       ▼                     │
│         ┌──────────────────────────────────────┐           │
│         │   Pydantic Schemas (Validation)       │           │
│         └──────────────────────────────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   BGE-M3    │  │   Qdrant    │  │ GPT-5-nano  │
│ Embeddings  │  │  Vector DB  │  │     LLM     │
│   (Local)   │  │ (Pre-loaded)│  │   (OpenAI)  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### Request Flow

**Chat Query:**
1. Client sends POST to `/chat` with natural language query
2. FastAPI validates request with `ChatRequest` schema
3. BGE-M3 generates query embedding (in-memory)
4. Qdrant performs similarity search on pre-loaded data
5. Context builder aggregates retrieved chunks
6. GPT-5-nano generates natural language response
7. Response includes answer + processing time metrics
8. FastAPI validates response with `ChatResponse` schema

## Performance

### Benchmarks
- **Embedding Generation**: Fast (BGE-M3, in-memory)
- **Vector Search**: Fast (Qdrant retrieval)
- **LLM Generation**: Moderate (GPT-5-nano, depends on response length)
- **Total Chat Latency**: Optimized for responsiveness
- **Startup**: Model loading time required (BGE-M3)

### Optimization
- ✅ Async operations throughout
- ✅ Connection pooling for Qdrant
- ✅ Efficient embedding batching
- ✅ Graceful error handling
- ✅ Request timeout protection

## Roadmap

- [x] **Phase 1: Preprocessing** - Markdown parsing & chunk creation
- [x] **Phase 2: Vectorization** - Embeddings generation & Qdrant vector DB
- [x] **Phase 3: RAG** - Semantic search + GPT-5-nano agent + RAGAS evaluation
- [x] **Phase 4: API Backend** - Production-ready REST API with comprehensive documentation
  - ✅ **Completed**: FastAPI REST endpoints (`/health`, `/chat`)
  - ✅ **Completed**: Scalar UI for interactive API documentation
  - ✅ **Completed**: Pydantic schemas with validation and examples
  - ✅ **Completed**: Error handling and performance metrics
  - ⏳ **Pending**: Basic frontend with shadcn/Astro
  - Rationale: Backend ready for frontend integration and real user validation
- [ ] **Phase 5: Quality & Testing** - Ruff linter + comprehensive test suite
  - Priority: Establishes safety net for rapid iteration
  - Scope: Ruff configuration, unit tests (preprocessing, embeddings, agent), integration tests
  - Rationale: Critical areas identified after real usage patterns emerge
- [ ] **Phase 6: Pipeline Optimization** - Iterative improvements based on metrics + user feedback
  - Priority: Data-driven enhancements to RAG components
  - Scope: Prompt engineering, reranking, dynamic TOP_K, context window optimization
  - Rationale: Optimize what matters to real users, guided by RAGAS metrics + production logs

## Deployment

### Production Checklist
- [ ] Set environment variables (`QDRANT_ENDPOINT`, `QDRANT_API_KEY`, `OPENAI_API_KEY`)
- [ ] Ensure Qdrant vector database is pre-loaded with portfolio data
- [ ] Configure firewall rules (allow port 8001 or configure reverse proxy)
- [ ] Set up monitoring for `/health` endpoint
- [ ] Configure log aggregation (optional: integrate with ELK/Datadog)
- [ ] Set up HTTPS with reverse proxy (nginx/Traefik)
- [ ] Allocate sufficient resources for BGE-M3 model (heavyweight)

### Docker
```bash
# Build
docker build -t portfolio-backend .

# Run (production mode: silent, ERROR logs only)
docker run -p 8001:8001 \
  -e QDRANT_ENDPOINT="your-endpoint" \
  -e QDRANT_API_KEY="your-key" \
  -e OPENAI_API_KEY="your-key" \
  portfolio-backend

# Run (development mode: verbose DEBUG logs)
docker run -p 8001:8001 \
  -e LOG_LEVEL=DEBUG \
  -e QDRANT_ENDPOINT="your-endpoint" \
  -e QDRANT_API_KEY="your-key" \
  -e OPENAI_API_KEY="your-key" \
  portfolio-backend
```

### Environment Configuration

**Development (verbose logs):**
```bash
export LOG_LEVEL=DEBUG
python -m src.portfolio.main
```

**Production (silent, errors only):**
```bash
export LOG_LEVEL=ERROR
uvicorn src.portfolio.api:app --host 0.0.0.0 --port 8001
```

## License

This project is licensed under the CC BY-NC 4.0 License - see the [LICENSE](LICENSE) file for details.

## Author

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/1024px-LinkedIn_icon.svg.png" alt="LinkedIn" width="14" style="margin-right: 5px;"> [**Cristian Sánchez Rodríguez**](https://www.linkedin.com/in/csanrod)
