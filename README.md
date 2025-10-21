# University Department Chatbot

A Flask-based chatbot application with LLM integration and RAG (Retrieval Augmented Generation) capabilities.

## Overview

This project provides a professional chatbot API built with Flask, featuring:

- RESTful API architecture with Flask blueprints
- **OpenRouter LLM integration** with Llama 3.3 70B (free tier available)
- Vector database for semantic search (ChromaDB, FAISS)
- Interactive API documentation with Swagger/OpenAPI
- Modular service layer architecture
- Session management for conversation tracking

## Project Structure

```
llm-practice/
├── run.py                      # Application entry point
├── requirment.txt              # Python dependencies
├── Makefile                    # Development commands
├── app/
│   ├── api/
│   │   ├── api.py              # Main API entry point (versioning)
│   │   └── v1/                 # Version 1 endpoints
│   │       ├── chat.py         # Chat endpoints
│   │       └── health.py       # Health & status endpoints
│   ├── models/                 # Database models
│   ├── services/
│   │   └── llm_service.py      # LLM integration service
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

### Quick Test

Test the chatbot API:
```bash
# Using the test script
python test_chat.py

# Or with cURL
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, who are you?"}'
```

See `API_QUICK_REFERENCE.md` for more examples and `API_VERSIONING_GUIDE.md` for API versioning details.

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

The project follows **professional API versioning** and modular architecture with clear separation of concerns:

- **API Layer** (`app/api/`) - Versioned RESTful endpoints (v1, v2, etc.)
  - `api.py` - Main entry point and version routing
  - `v1/` - Version 1 endpoints (isolated and independent)
- **Service Layer** (`app/services/`) - Business logic and LLM integration
- **Model Layer** (`app/models/`) - Database models and schemas
- **Configuration** (`config/`) - Application settings and environment management

This architecture enables:
- ✅ **API Versioning** - Support multiple API versions simultaneously
- ✅ **Backward Compatibility** - Old clients continue working when new versions are released
- ✅ **Independent Evolution** - Each version evolves independently
- ✅ **Professional Standard** - Following industry best practices (Stripe, GitHub, Twitter)

## API Endpoints

The API follows **professional versioning best practices** with URL-based versioning (`/api/v1/`, `/api/v2/`, etc.).

### General Endpoints
- `GET /` - Welcome message and endpoint information
- `GET /api` - API root with version information
- `GET /apidocs` - Interactive API documentation (Swagger UI)
- `GET /apispec.json` - OpenAPI specification

### Version 1 Endpoints
- `GET /api/v1/health` - Health check
- `GET /api/v1/status` - API status and configuration
- `POST /api/v1/chat/message` - Send a message to the chatbot
- `GET /api/v1/chat/models` - Get current model information

See `API_QUICK_REFERENCE.md` for detailed examples and `API_VERSIONING_GUIDE.md` for versioning strategy.

## Features

- **RESTful API** - Clean, well-structured API endpoints
- **OpenRouter Integration** - Free access to Llama 3.3 70B and other models
- **Conversation Tracking** - Session management for multi-turn conversations
- **Vector Search** - Semantic search using RAG (planned)
- **API Documentation** - Interactive Swagger UI
- **Authentication** - JWT-based authentication (planned)
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