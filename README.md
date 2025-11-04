# IBIT Chatbot - BIT Chatter 🤖

A professional AI-powered chatbot for the Institute of Business and Information Technology (IBIT) at Punjab University Lahore. Built with **RAG (Retrieval-Augmented Generation)** and **FAISS vector database** for accurate, context-aware responses.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenRouter API Key (get free at https://openrouter.ai/)

### Setup (3 Steps)

**1. Activate Virtual Environment**
```bash
cd /home/dev/Desktop/llm-practice
source venv/bin/activate
```

**2. Configure API Key**
```bash
# Copy example config
cp env.example .env

# Edit and add your OpenRouter API key
nano .env  # or use vim, gedit, etc.
```

In `.env`, replace:
```
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

**3. Run the Application**
```bash
python run.py
```

**Open:** http://localhost:5000

That's it! 🎉

## ✨ Features

- ✅ **Vector Database** - 581 vectors from 257 intents (FAISS)
- ✅ **RAG System** - Accurate, context-aware responses
- ✅ **Professional LLM** - Formal, well-structured answers (Llama 3.3 70B)
- ✅ **Beautiful UI** - Dark/light mode, responsive design
- ✅ **REST API** - Full API with Swagger documentation
- ✅ **Session Management** - Conversation history tracking

## 🧪 Verify Setup

```bash
python verify_setup.py
```

This checks:
- ✓ Dependencies installed
- ✓ Vector database working
- ✓ Database initialized
- ✓ Data file loaded
- ⚠ API key configured

## 🎯 Try These Queries

- "What is IBIT?"
- "Tell me about the BBIT program"
- "What courses are offered?"
- "How can I get admission?"
- "What is the fee structure?"
- "Tell me about faculty members"

## 📁 Project Structure

```
llm-practice/
├── app/
│   ├── api/              # REST API routes
│   ├── core/             # LLM engine
│   ├── services/         # RAG & chat services
│   ├── web/              # Web routes
│   ├── models/           # Database models
│   └── utils/            # Vector DB utilities
├── data/
│   ├── Ibit_data.json    # Knowledge base (257 intents)
│   └── vector_db/        # FAISS index (auto-generated)
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── requirements.txt     # Dependencies
└── run.py              # Entry point
```

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Required
OPENROUTER_API_KEY=your-api-key-here

# Optional (defaults shown)
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///instance/app.db
LOG_LEVEL=INFO
```

### Get API Key
1. Go to https://openrouter.ai/
2. Sign up (free!)
3. Get API key from dashboard
4. Add to `.env`

## 🌐 API Endpoints

### Web Interface
- `GET /` - Main chatbot UI
- `POST /get_response` - Chat endpoint for UI

### REST API
- `POST /api/v1/chat/message` - Send message
- `GET /api/v1/chat/session/<id>` - Get session messages
- `POST /api/v1/chat/session` - Create session
- `GET /api/v1/health` - Health check

### API Documentation
When running, visit: http://localhost:5000/apidocs

### Example API Request

```bash
curl -X POST http://localhost:5000/get_response \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What is IBIT?"}'
```

```bash
curl -X POST http://localhost:5000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about BBIT program",
    "temperature": 0.7
  }'
```

## 🏗️ Architecture

```
User Query
    ↓
Web Interface (React-like UI)
    ↓
Flask Routes (/get_response)
    ↓
RAG Service
    ├─→ Vector DB (FAISS) → Semantic Search
    │   └─→ Retrieves relevant context
    └─→ LLM Engine (OpenRouter)
        └─→ Generates professional response
    ↓
Professional, Accurate Answer
```

### How RAG Works

1. **User asks question** → "What is IBIT?"
2. **Vector search** → Finds 5 most relevant contexts from knowledge base
3. **Context augmentation** → Adds retrieved info to LLM prompt
4. **LLM generation** → Creates professional, accurate response
5. **User receives** → Formal, well-structured answer

## 🎨 UI Features

- 🌙 **Dark/Light Mode** - Click sun/moon icon
- 💬 **Real-time Chat** - Typing animation
- 📱 **Responsive** - Works on mobile & desktop
- 💾 **Chat History** - Saved in browser
- 📋 **Copy Responses** - Click copy icon
- 🗑️ **Clear Chat** - Delete conversation

## 🔄 Adding New Knowledge

1. **Edit data file:**
```bash
nano data/Ibit_data.json
```

2. **Add new intent:**
```json
{
  "tag": "new_topic",
  "patterns": [
    "Question 1",
    "Question 2",
    "Question 3"
  ],
  "responses": [
    "Professional answer here."
  ]
}
```

3. **Rebuild vector database:**
```bash
python build_vector_db.py
```

4. **Restart application**

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Vector database not found"
```bash
python build_vector_db.py
```

### "API key error"
```bash
# Check .env file exists and has valid key
cat .env | grep OPENROUTER_API_KEY
```

### "Port 5000 in use"
```bash
# Use different port
python -c "from app.main import create_app; app=create_app(); app.run(port=5001)"
```

### "Database error"
```bash
# Reset database
rm instance/app.db
python -c "from app.main import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all()"
```

## 📊 Knowledge Base

Your chatbot has knowledge about:

| Category | Topics |
|----------|--------|
| **IBIT Info** | Overview, history, vision, mission, location |
| **Programs** | BBIT, MBIT, specializations, duration |
| **Admissions** | Requirements, process, deadlines, eligibility |
| **Courses** | Syllabus, descriptions, credits, prerequisites |
| **Faculty** | Professors, departments, expertise |
| **Facilities** | Labs, library, sports, hostels, cafeteria |
| **Fees** | Structure, payment plans, scholarships |
| **Exams** | Schedule, rules, results, grading |
| **Placements** | Companies, opportunities, statistics |
| **Campus Life** | Events, societies, activities, clubs |

**Total:** 257 intent categories with 581 query patterns

## 🚀 Production Deployment

### Using Gunicorn

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Set production environment
export FLASK_ENV=production

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app.main:create_app()" --timeout 120
```

### Environment Setup

For production, update `.env`:
```env
FLASK_ENV=production
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=postgresql://... # For production DB
LOG_LEVEL=WARNING
```

## 📈 Performance

| Metric | Value |
|--------|-------|
| **Vector Search** | < 50ms |
| **Response Time** | 2-5 seconds |
| **Memory Usage** | ~500MB |
| **Concurrent Users** | Multiple supported |
| **Database** | 581 vectors, 257 intents |
| **Accuracy** | Grounded in knowledge base |

## 🛠️ Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest
pytest --cov=app tests/
```

### Code Quality
```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/
```

### Rebuild Vector Database
```bash
python build_vector_db.py --test-query "What is IBIT?"
```

## 🔐 Security

- API key stored in environment variables (never in code)
- CORS configured
- Input validation on all endpoints
- Error handling prevents information leakage
- Session management with secure IDs

## 📚 Technical Stack

### Backend
- **Framework:** Flask 3.0.3
- **LLM:** OpenRouter API (Llama 3.3 70B Instruct)
- **Vector DB:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Database:** SQLite with SQLAlchemy ORM

### Frontend
- **HTML5** with modern CSS
- **JavaScript** (Vanilla)
- **Responsive Design**
- **Dark/Light Mode**

### Key Libraries
```
faiss-cpu==1.9.0
sentence-transformers==3.3.1
Flask==3.0.3
Flask-CORS==5.0.0
Flask-SQLAlchemy==3.1.1
openai==2.2.0
```

## 🎓 Learning Resources

This project demonstrates:

- ✅ **RAG (Retrieval-Augmented Generation)** - Complete implementation
- ✅ **Vector Databases** - FAISS with semantic search
- ✅ **LLM Integration** - OpenRouter API usage
- ✅ **Flask Web Framework** - Modern app structure
- ✅ **REST API Design** - Best practices
- ✅ **SQLAlchemy ORM** - Database modeling
- ✅ **Production Code** - Error handling, logging, security

## 📝 Useful Commands

```bash
# Verify everything is working
python verify_setup.py

# Rebuild vector database
python build_vector_db.py

# Run application
python run.py

# Run with different port
python -c "from app.main import create_app; app=create_app(); app.run(port=5001)"

# Initialize database
python -c "from app.main import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all()"

# Test vector search (no API key needed)
python -c "
from app.utils.vector_db import FAISSVectorDB
vdb = FAISSVectorDB()
vdb.load('data/vector_db/faiss.index', 'data/vector_db/metadata.pkl', 'data/vector_db/config.json')
results = vdb.search('What is IBIT?', k=3)
for r in results:
    print(f\"{r['metadata']['tag']}: {r['score']:.3f}\")
"
```

## ❓ FAQ

**Q: Do I need a paid API key?**
A: No! OpenRouter offers free tier with Llama 3.3 70B.

**Q: Can I use a different LLM?**
A: Yes! Set `OPENROUTER_MODEL` in `.env` to any OpenRouter model.

**Q: How do I add more questions?**
A: Edit `data/Ibit_data.json`, add new intents, rebuild vector DB.

**Q: Can I deploy this online?**
A: Yes! Works with any Python hosting (Heroku, AWS, DigitalOcean, etc.)

**Q: Is the data secure?**
A: Yes! API keys in env vars, no data sent except to OpenRouter for LLM.

**Q: How accurate are responses?**
A: Very! RAG ensures answers are grounded in your knowledge base.

## 🤝 Contributing

To add new features:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📧 Support

For issues:
- Check this README troubleshooting section
- Run `python verify_setup.py` for diagnostics
- Check logs for error messages
- Visit API docs at `/apidocs` when running

## 📜 License

[Add your license here]

## 👥 Credits

- **IBIT, Punjab University Lahore** - Knowledge base
- **OpenRouter** - LLM API
- **FAISS** - Vector search
- **Sentence Transformers** - Embeddings

---

## 🎉 Ready to Use!

**Current Status:** ✅ Production Ready

**Setup Checklist:**
- [ ] Virtual environment activated
- [ ] `.env` file created
- [ ] OpenRouter API key added to `.env`
- [ ] Run `python verify_setup.py` ✓
- [ ] Start with `python run.py`
- [ ] Open http://localhost:5000
- [ ] Test with a query!

**Everything is configured and ready to go! Just add your API key and start chatting! 🚀**

Made with ❤️ for IBIT students and staff
