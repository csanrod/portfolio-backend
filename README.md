# Portfolio Backend

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

RAG-powered backend for an intelligent portfolio chatbot. Built to showcase end-to-end AI implementation using modern Python practices.

## Overview

This backend implements a Retrieval-Augmented Generation (RAG) system that powers an interactive portfolio chatbot. It processes professional information and enables natural language queries about experience, skills, and projects.

## Features

- **RAG Pipeline**: Semantic search over portfolio documentation
- **Simple Architecture**: Clean, maintainable Python codebase
- **Production Ready**: Follows Python packaging standards

## Project Structure

```
portfolio-backend/
├── src/
│   └── portfolio/          # Main package
│       ├── __init__.py     # Package initialization
│       └── main.py         # Entry point
├── docs/                   # Documentation and RAG data
│   └── info_portfolio.md   # Portfolio content for ingestion
├── .gitignore              # Python gitignore template
├── LICENSE                 # CC BY-NC 4.0
├── README.md               # This file
├── CHANGELOG.md            # Version history
└── requirements.txt        # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/portfolio-backend.git
cd portfolio-backend

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python -m src.portfolio.main
```

## Development

This project follows [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching strategy:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `hotfix/*` - Production fixes

## Documentation

All project documentation and RAG ingestion data is located in the `docs/` directory.

## License

This project is licensed under the CC BY-NC 4.0 License - see the [LICENSE](LICENSE) file for details.

## Author

**Cristian Sánchez Rodríguez**
- GitHub: [@csanrod](https://github.com/csanrod)
- LinkedIn: [Cristian Sánchez Rodríguez](https://www.linkedin.com/in/csanrod)
