# Personalized Document Response System
## 3-LLM Agent Pipeline with GPT-5 Integration

> **Live Demo**: [https://web-production-5c5b4.up.railway.app](https://web-production-5c5b4.up.railway.app)

An agentic service that automates internal document requests through intelligent security checks and personalized email generation, powered by OpenAI's GPT-5.

---

## 🎯 What It Does

When a user emails requesting a document, the system automatically:

1. **🔍 Doc Finder Agent** - Analyzes the request and searches for relevant documents
2. **🔒 Security Agent** - Validates permissions based on role, clearance level, and tenure
3. **✍️ Response Generator** - Crafts a personalized approval or denial email

**Result**: Instant, secure document responses that save time and increase security.

### Live Example

**Request:**
```json
{
  "sender": "john.doe@company.com",
  "body": "I need the API documentation"
}
```

**Response:** *(Complete agent visibility)*
```json
{
  "success": true,
  "agent_steps": [
    {"agent": "Doc Finder", "data": {"search_query": "API documentation", "documents_found": 1}},
    {"agent": "Security Check", "data": {"decision": "approved", "reasoning": "User has standard clearance"}},
    {"agent": "Response Generator", "data": {"email_response": "Here's the API documentation..."}}
  ],
  "final_response": "Thanks — I've provided the API documentation...",
  "approved_document": {
    "name": "API Documentation v2.1",
    "url": "https://docs.google.com/document/d/def456"
  }
}
```

---

## 🚀 Tech Stack

- **AI Model**: OpenAI GPT-5-mini (400K context, 128K output)
- **Backend**: Flask + Python 3.12
- **Deployment**: Railway (auto-deploy from GitHub)
- **Frontend**: CORS-enabled REST API (compatible with any frontend)

---

## 📋 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/harshith998/Personalized_DB.git
cd Personalized_DB
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create `.env` file:
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run Locally
```bash
python app.py
# Server runs on http://localhost:8000
```

### 4. Test It
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"sender":"john.doe@company.com","body":"I need the API documentation"}'
```

---

## 🌐 API Endpoints

### `GET /` - Service Info
```bash
curl https://web-production-5c5b4.up.railway.app/
```
Returns service metadata, available endpoints, and agent descriptions.

### `GET /health` - Health Check
```bash
curl https://web-production-5c5b4.up.railway.app/health
# Response: {"status": "healthy"}
```

### `GET /demo-scenarios` - Get Demo Scenarios
Returns 3 pre-configured test scenarios:
- ✅ **Approved Request**: Senior Engineer → API Documentation
- ❌ **Denied Request**: Intern → Q4 Financial Report
- 🔐 **Executive Access**: CFO → Q4 Financial Report

Perfect for testing your frontend integration!

### `POST /process` - Process Email (Main Endpoint)
Runs the complete 3-agent pipeline and returns structured results.

**Request:**
```json
{
  "sender": "user@example.com",
  "subject": "Document Request",  // optional
  "body": "I need the API documentation"
}
```

**Response:** Includes `agent_steps`, `final_response`, `approved_document`, `user_profile`, and `request` details.

---

## 🎨 Frontend Integration

**Complete integration guide**: [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)

Includes:
- Visual mockup (Linear-inspired design)
- TypeScript types
- React component code
- API service layer
- Demo flow recommendations
- Styling examples

### Quick Integration Example
```typescript
const response = await fetch('https://web-production-5c5b4.up.railway.app/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sender: 'john.doe@company.com',
    body: 'I need the API documentation'
  })
});

const data = await response.json();
// Display: data.agent_steps, data.final_response, data.approved_document
```

---

## 🤖 GPT-5 Integration

Upgraded from GPT-4 to **GPT-5-mini** for:
- 💰 **Lower cost** ($0.25/1M vs $5/1M input tokens)
- 🚀 **Larger context** (400K tokens vs 128K)
- 🎯 **Better reasoning** (built-in reasoning capabilities)

**Key API Changes:**
```python
# GPT-4 (old)
max_tokens=500

# GPT-5 (new)
max_completion_tokens=7000
```

Full details: [GPT5_INTEGRATION.md](GPT5_INTEGRATION.md)

---

## 📁 Project Structure

```
Personalized_DB/
├── app.py                  # Flask API server (CORS, routes)
├── pipeline.py             # Main orchestration (runs 3 agents)
├── config.py               # GPT-5 configuration
├── agents/
│   ├── doc_finder.py       # Agent 1: Finds documents
│   ├── security.py         # Agent 2: Checks permissions
│   └── response_generator.py # Agent 3: Writes emails
├── data/
│   ├── mongodb.py          # User profiles (mock)
│   └── supermemory.py      # Document search (mock)
├── requirements.txt        # Dependencies
├── Procfile               # Railway deployment
├── .env                   # API keys (gitignored)
├── FRONTEND_GUIDE.md      # Frontend integration
├── GPT5_INTEGRATION.md    # GPT-5 upgrade guide
└── README.md              # This file
```

---

## 🔐 Security Model

### User Clearance Levels
- **Limited**: Interns, contractors (access public docs only)
- **Standard**: Engineers (access internal docs)
- **Executive**: C-suite (access confidential docs)

### Permission Check Logic
```python
if user.clearance >= document.required_clearance:
    approve()
else:
    deny()
```

Security agent also considers:
- User role and department
- Tenure (how long they've been at company)
- Principle of least privilege

---

## 📊 Demo Scenarios

| Scenario | User | Clearance | Request | Document Clearance | Result |
|----------|------|-----------|---------|-------------------|--------|
| 1 | Senior Engineer | Standard | API Docs | Standard | ✅ Approved |
| 2 | Intern | Limited | Financial Report | Executive | ❌ Denied |
| 3 | CFO | Executive | Financial Report | Executive | ✅ Approved |

Access via: `GET /demo-scenarios`

---

## 🚢 Deployment

### Railway (Production)
1. Push to GitHub: `git push`
2. Railway auto-deploys from `main` branch
3. Set `OPENAI_API_KEY` in Railway dashboard
4. Done! API live at: https://web-production-5c5b4.up.railway.app

### Local Development
```bash
# Use different port if 8000 is taken
PORT=8080 python app.py
```

---

## 📝 Customization

### Add New Documents
Edit `data/supermemory.py`:
```python
mock_docs.append({
    "id": "doc_005",
    "name": "Engineering Playbook",
    "url": "https://docs.google.com/...",
    "required_clearance": "standard"
})
```

### Add New Users
Edit `data/mongodb.py`:
```python
mock_users["newuser@company.com"] = {
    "name": "New User",
    "role": "Engineer",
    "clearance": "standard",
    "tenure_months": 12
}
```

### Change AI Model
Edit `config.py`:
```python
# Options: "gpt-5", "gpt-5-mini", "gpt-5-nano"
OPENAI_MODEL = "gpt-5"  # Higher quality, higher cost
```

---

## 🐛 Troubleshooting

### 500 Error: "max_tokens not supported"
**Cause**: Using old GPT-4 parameter
**Fix**: Ensure `max_completion_tokens` is used (already fixed in code)

### CORS Error in Frontend
**Cause**: Browser blocking cross-origin requests
**Fix**: CORS is already enabled for `*` origins. Clear browser cache.

### "OPENAI_API_KEY not set"
**Local**: Add to `.env` file
**Railway**: Add in Railway dashboard → Variables tab

### Slow First Request
**Cause**: Railway cold start (free tier)
**Fix**: Normal behavior. Subsequent requests are fast.

---

## 📚 Documentation

- **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** - Complete frontend integration (React/TypeScript examples, API docs, component code)
- **[GPT5_INTEGRATION.md](GPT5_INTEGRATION.md)** - GPT-5 upgrade details (model comparison, API changes, testing)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Railway deployment guide (step-by-step with screenshots)

---

## ✨ Features

- ✅ 3 intelligent LLM agents working in pipeline
- ✅ OpenAI GPT-5-mini integration (400K context)
- ✅ Role-based access control with clearance levels
- ✅ Complete agent step visibility for debugging
- ✅ CORS-enabled REST API for any frontend
- ✅ Pre-configured demo scenarios
- ✅ Railway auto-deployment from GitHub
- ✅ Comprehensive documentation with code examples
- ✅ Mock data (no database required for testing)
- ✅ Environment variable configuration
- ✅ Error handling with detailed tracebacks

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Create Pull Request

---

## 📄 License

MIT License - Free to use for your projects!

---

## 🔗 Links

- **Live API**: https://web-production-5c5b4.up.railway.app
- **GitHub**: https://github.com/harshith998/Personalized_DB
- **Railway Dashboard**: https://railway.app
- **OpenAI Platform**: https://platform.openai.com

---

**Built with GPT-5 and deployed on Railway** 🚂
*Automating internal document requests with intelligent agents*
