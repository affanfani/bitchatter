# University Department Chatbot

A Flask-based chatbot application with LLM integration and RAG (Retrieval Augmented Generation) capabilities.

## Overview

This project provides a professional chatbot API built with Flask, featuring:

- RESTful API architecture with Flask blueprints
- LLM integration with multiple providers (OpenAI, Ollama, OpenRouter)
- Vector database for semantic search (ChromaDB, FAISS)
- Interactive API documentation with Swagger/OpenAPI
- Modular service layer architecture

## Project Structure

```
llm-practice/
├── run.py                      # Application entry point
├── requirment.txt              # Python dependencies
├── Makefile                    # Development commands
├── app/
│   ├── api/                    # API routes and blueprints
│   ├── models/                 # Database models
│   ├── services/               # Business logic (LLM, Vector DB)
│   ├── utils/                  # Helper functions
│   ├── static/                 # Static assets
│   └── templates/              # HTML templates
├── config/
│   ├── __init__.py             # Configuration classes
│   └── swagger_config.py       # API documentation config
├── data/                       # Application data
├── tests/                      # Test suite
└── docs/                       # Documentation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation
1. Clone the repository and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirment.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application:
```bash
python run.py
```

The application will start at `http://localhost:5000`

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:5000/apidocs`
- **OpenAPI Spec**: `http://localhost:5000/apispec.json`

## Development Commands

Using the Makefile:
```bash
make install       # Install dependencies
make run           # Start development server
make test          # Run tests
make lint          # Check code quality
make clean         # Clean cache files
```

## Key Technologies

### Backend Framework
- **Flask 3.0.3** - Lightweight web framework
- **Flasgger 0.9.7.1** - Swagger/OpenAPI documentation

### Database & ORM
- **SQLAlchemy** - Database ORM
- **Flask-Migrate** - Database migrations
- **PostgreSQL/SQLite** - Database support

### AI/ML Stack
- **LangChain** - LLM framework
- **OpenAI/Ollama** - LLM providers
- **ChromaDB** - Vector database for RAG
- **Sentence-Transformers** - Text embeddings
- **FAISS** - Vector similarity search

### Additional Features
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-JWT-Extended** - Authentication
- **Flask-Limiter** - Rate limiting
- **Celery** - Background task processing
- **Redis** - Caching and sessions

## Architecture

The project follows a modular architecture with clear separation of concerns:

- **API Layer** (`app/api/`) - RESTful endpoints and request handling
- **Service Layer** (`app/services/`) - Business logic and LLM integration
- **Model Layer** (`app/models/`) - Database models and schemas
- **Configuration** (`config/`) - Application settings and environment management

## Features

- **RESTful API** - Clean, well-structured API endpoints
- **LLM Integration** - Support for multiple LLM providers
- **Vector Search** - Semantic search using RAG
- **API Documentation** - Interactive Swagger UI
- **Authentication** - JWT-based authentication
- **Rate Limiting** - Request throttling for API protection
- **Database Support** - PostgreSQL and SQLite
- **Background Tasks** - Async processing with Celery
- **Testing** - Comprehensive test suite

## Testing

Run tests using:
```bash
make test
# or
pytest
```

Run tests with coverage:
```bash
make test-cov
# or
pytest --cov=app tests/
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub: [github.com/affanfani/bitchatter](https://github.com/affanfani/bitchatter)