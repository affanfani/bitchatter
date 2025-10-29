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

**Note**: The vector database is automatically built on first startup from `data/Ibit_data.json`. 
No manual setup required! Subsequent starts will load the existing database instantly.

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
make install         # Install dependencies
make run             # Start development server
make test            # Run tests
make lint            # Check code quality
make clean           # Clean cache files
make build-vectors   # Build FAISS vector database
make rebuild-vectors # Rebuild vector database
make clean-vectors   # Remove vector database files
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

#### Health & Status
- `GET /api/v1/health` - Health check
- `GET /api/v1/status` - API status and configuration

#### Chat
- `POST /api/v1/chat/message` - Send a message to the chatbot
- `POST /api/v1/chat/session` - Create a new chat session
- `GET /api/v1/chat/session/<session_id>` - Get messages for a session

#### Intent Matching (NEW! 🎉)
- `POST /api/v1/intent/match` - Match user query to the most relevant intent
- `POST /api/v1/intent/search` - Search for multiple matching intents
- `POST /api/v1/intent/response` - Get direct response based on matched intent
- `GET /api/v1/intent/stats` - Get vector database statistics

See `API_QUICK_REFERENCE.md` for detailed examples and `API_VERSIONING_GUIDE.md` for versioning strategy.

## Features

- **RESTful API** - Clean, well-structured API endpoints
- **OpenRouter Integration** - Free access to Llama 3.3 70B and other models
- **Conversation Tracking** - Session management for multi-turn conversations
- **Vector Search** - FAISS-based semantic search for intent matching
- **Intent Matching** - Automatic intent detection using sentence-transformers
- **API Documentation** - Interactive Swagger UI
- **Authentication** - JWT-based authentication (planned)
- **Rate Limiting** - Request throttling for API protection
- **Database Support** - PostgreSQL and SQLite
- **Background Tasks** - Async processing with Celery
- **Testing** - Comprehensive test suite

## Vector Database & Intent Matching

The project includes **automatic FAISS vector database initialization** for fast semantic search and intent matching.

### 🎯 Automatic Setup

**No manual setup required!** The vector database is automatically:
- ✅ Built on first server startup from `data/Ibit_data.json`
- ✅ Loaded instantly on subsequent startups
- ✅ Shared across all services and endpoints

Just run `python run.py` and the system handles everything!

### Manual Rebuild (Optional)

If you need to manually rebuild the vector database:
```bash
# Remove and rebuild
make rebuild-vectors

# Or just rebuild
make build-vectors
```

### Using Intent Matching API

The server provides RESTful endpoints for intent matching:

```bash
# Match a user query to an intent
curl -X POST http://localhost:5000/api/v1/intent/match \
  -H "Content-Type: application/json" \
  -d '{"query": "What courses are available?"}'

# Get direct response based on matched intent
curl -X POST http://localhost:5000/api/v1/intent/response \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}'

# Search for multiple matching intents
curl -X POST http://localhost:5000/api/v1/intent/search \
  -H "Content-Type: application/json" \
  -d '{"query": "admission requirements", "k": 5}'

# Get vector database statistics
curl http://localhost:5000/api/v1/intent/stats
```

### Using Intent Matcher in Code

```python
from flask import current_app
from app.services.intent_matcher import create_intent_matcher

# In your Flask route or service
intent_matcher = create_intent_matcher(current_app)

# Get response for user query
response = intent_matcher.get_response("Hello!")

# Get intent tag
tag = intent_matcher.get_intent_tag("What is your name?")

# Match intent with confidence score
result = intent_matcher.match_intent("tell me about courses")
if result:
    print(f"Tag: {result['metadata']['tag']}")
    print(f"Confidence: {result['score']}")

# Search with multiple results
matches = intent_matcher.search_intents("admission info", k=5)
```

### Direct Vector Database Access

```python
from flask import current_app

# Access the pre-loaded vector database
vector_db = current_app.config.get('VECTOR_DB')

if vector_db:
    # Search for similar texts
    results = vector_db.search("programming courses", k=5)
    
    # Get database statistics
    stats = vector_db.get_stats()
    print(f"Vectors: {stats['total_vectors']}")
```

### Key Components
- **`app/main.py`** - Automatic vector DB initialization on startup
- **`app/utils/vector_db.py`** - FAISS vector database utility
- **`app/services/intent_matcher.py`** - Intent matching service
- **`app/api/v1/routes/intent_routes.py`** - Intent matching API endpoints
- **`build_vector_db.py`** - Manual build script (optional)
- **`data/vector_db/`** - Generated FAISS index and metadata

### Configuration

Customize vector database settings in your Flask config:

```python
# In config/base.py or config/development.py
VECTOR_DB_PATH = 'data/vector_db'
INTENT_MATCH_THRESHOLD = 0.5  # Minimum similarity score (0-1)
```

For more details, see **`VECTOR_DB_SETUP.md`**

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