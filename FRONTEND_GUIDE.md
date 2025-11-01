# Frontend Integration Guide
## Personalized Document Response System

> **Backend URL:** `https://web-production-5c5b4.up.railway.app`

---

## 📐 Visual Design Mockup

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🤖 Personalized Document Response System                              │
│                                                                         │
├──────────────────────────┬──────────────────────────────────────────────┤
│                          │                                              │
│  📧 EMAIL REQUEST        │  🔄 AGENT PROCESSING                         │
│                          │                                              │
│  ┌────────────────────┐  │  ┌────────────────────────────────────────┐ │
│  │ From:              │  │  │ 🔍 Doc Finder            [COMPLETE]    │ │
│  │ [Dropdown ▼]       │  │  │ ├─ Query: "API documentation"          │ │
│  │                    │  │  │ └─ Found 2 documents                   │ │
│  │ john.doe@...       │  │  └────────────────────────────────────────┘ │
│  │ intern@...         │  │                                              │
│  │ cfo@...            │  │  ┌────────────────────────────────────────┐ │
│  └────────────────────┘  │  │ 🔒 Security Check        [COMPLETE]    │ │
│                          │  │ ├─ Decision: ✅ APPROVED               │ │
│  Subject:                │  │ ├─ User: Senior Engineer               │ │
│  ┌────────────────────┐  │  │ └─ Clearance: Standard                │ │
│  │ Document Request   │  │  └────────────────────────────────────────┘ │
│  └────────────────────┘  │                                              │
│                          │  ┌────────────────────────────────────────┐ │
│  Body:                   │  │ ✍️  Response Generator   [COMPLETE]    │ │
│  ┌────────────────────┐  │  │ └─ Email crafted successfully          │ │
│  │ I need the API     │  │  └────────────────────────────────────────┘ │
│  │ documentation...   │  │                                              │
│  │                    │  │  ─────────────────────────────────────────── │
│  │                    │  │                                              │
│  │                    │  │  ✉️  GENERATED RESPONSE                      │
│  └────────────────────┘  │                                              │
│                          │  ┌────────────────────────────────────────┐ │
│  [Quick Demos ▼]         │  │ To: john.doe@company.com               │ │
│  ┌────────────────────┐  │  │ Re: API Documentation Request          │ │
│  │ ✅ Approved        │  │  │                                        │ │
│  │ ❌ Denied          │  │  │ Hi John,                               │ │
│  │ 🔐 Executive       │  │  │                                        │ │
│  └────────────────────┘  │  │ I've got the API Documentation v2.1    │ │
│                          │  │ you requested. Here's the link:        │ │
│  ┌────────────────────┐  │  │                                        │ │
│  │  PROCESS REQUEST   │  │  │ 🔗 API Documentation v2.1              │ │
│  └────────────────────┘  │  │                                        │ │
│                          │  │ This covers all the REST API           │ │
│                          │  │ endpoints and authentication.          │ │
│                          │  └────────────────────────────────────────┘ │
│                          │                                              │
│                          │  📄 DOCUMENT PREVIEW                         │
│                          │  [Google Doc style preview if approved]     │
└──────────────────────────┴──────────────────────────────────────────────┘
```

---

## 🎨 Design System (Linear-inspired)

### Colors
```css
/* Light Mode */
--background: #fafafa;
--surface: #ffffff;
--border: #e5e7eb;
--text-primary: #18181b;
--text-secondary: #71717a;
--accent: #8b5cf6; /* Purple */
--success: #22c55e;
--error: #ef4444;

/* Dark Mode */
--background: #18181b;
--surface: #27272a;
--border: #3f3f46;
--text-primary: #fafafa;
--text-secondary: #a1a1aa;
```

### Typography
```css
font-family: 'Inter', -apple-system, system-ui, sans-serif;

/* Headings */
h1: 24px, 600
h2: 20px, 600
h3: 16px, 600

/* Body */
body: 14px, 400
small: 12px, 400
```

### Components
- **Cards:** Subtle border, slight shadow, 8px border-radius
- **Buttons:** 6px border-radius, 10px padding, subtle hover
- **Agent Steps:** Glass-morphism effect, icon + status badge

---

## 🔌 API Documentation

### Base URL
```
https://web-production-5c5b4.up.railway.app
```

### Endpoints

#### 1. GET `/` - Service Info
```bash
curl https://web-production-5c5b4.up.railway.app/
```

**Response:**
```json
{
  "service": "Personalized Document Response System",
  "description": "3-LLM Agent Pipeline for Secure Document Requests",
  "status": "running",
  "version": "2.0.0",
  "endpoints": {...},
  "agents": [...]
}
```

---

#### 2. GET `/demo-scenarios` - Get Demo Scenarios
```bash
curl https://web-production-5c5b4.up.railway.app/demo-scenarios
```

**Response:**
```json
{
  "scenarios": [
    {
      "id": "approved_standard",
      "name": "✅ Approved Request (Standard User)",
      "description": "Senior Engineer requests API documentation",
      "request": {
        "sender": "john.doe@company.com",
        "subject": "API Documentation Request",
        "body": "Hey, I need the API documentation..."
      },
      "expected_outcome": "Approved - User has standard clearance"
    }
  ],
  "available_users": [...]
}
```

---

#### 3. POST `/process` - Process Email Request
```bash
curl -X POST https://web-production-5c5b4.up.railway.app/process \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "john.doe@company.com",
    "subject": "API Documentation Request",
    "body": "I need the API documentation"
  }'
```

**Request Body:**
```typescript
{
  sender: string;      // Required - Email address
  subject?: string;    // Optional - Defaults to "Document Request"
  body: string;        // Required - Email body
}
```

**Success Response (200):**
```json
{
  "success": true,
  "agent_steps": [
    {
      "agent": "Doc Finder",
      "status": "complete",
      "icon": "🔍",
      "data": {
        "search_query": "API documentation",
        "request_type": "documentation",
        "documents_found": 2,
        "documents": [
          {
            "id": "doc_002",
            "name": "API Documentation v2.1",
            "url": "https://docs.google.com/document/d/def456",
            "description": "REST API endpoints...",
            "sensitivity": "internal",
            "required_clearance": "standard"
          }
        ],
        "llm_reasoning": "{\"search_query\":...}"
      }
    },
    {
      "agent": "Security Check",
      "status": "complete",
      "icon": "🔒",
      "data": {
        "decision": "approved",
        "reasoning": "User has standard clearance...",
        "user_clearance": "standard",
        "user_role": "Senior Engineer",
        "selected_doc": "doc_002"
      }
    },
    {
      "agent": "Response Generator",
      "status": "complete",
      "icon": "✍️",
      "data": {
        "email_response": "Hi John, I've got the API Documentation...",
        "response_type": "approved",
        "document_provided": true
      }
    }
  ],
  "final_response": "Hi John, I've got the API Documentation v2.1...",
  "approved_document": {
    "id": "doc_002",
    "name": "API Documentation v2.1",
    "url": "https://docs.google.com/document/d/def456",
    "description": "REST API endpoints...",
    "sensitivity": "internal",
    "required_clearance": "standard"
  },
  "user_profile": {
    "name": "John Doe",
    "role": "Senior Engineer",
    "clearance": "standard"
  },
  "request": {
    "sender": "john.doe@company.com",
    "subject": "API Documentation Request",
    "body": "I need the API documentation"
  }
}
```

**Error Response (400/500):**
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## 💻 React/TypeScript Implementation

### 1. Types
```typescript
// types.ts
export interface AgentStep {
  agent: string;
  status: 'complete' | 'processing' | 'error';
  icon: string;
  data: {
    [key: string]: any;
  };
}

export interface Document {
  id: string;
  name: string;
  url: string;
  description: string;
  sensitivity: string;
  required_clearance: string;
}

export interface ProcessResponse {
  success: boolean;
  agent_steps: AgentStep[];
  final_response: string;
  approved_document: Document | null;
  user_profile: {
    name: string;
    role: string;
    clearance: string;
  };
  request: {
    sender: string;
    subject: string;
    body: string;
  };
}

export interface DemoScenario {
  id: string;
  name: string;
  description: string;
  request: {
    sender: string;
    subject: string;
    body: string;
  };
  expected_outcome: string;
}
```

### 2. API Service
```typescript
// api.ts
const API_BASE = 'https://web-production-5c5b4.up.railway.app';

export const api = {
  async getDemoScenarios(): Promise<{ scenarios: DemoScenario[] }> {
    const res = await fetch(`${API_BASE}/demo-scenarios`);
    if (!res.ok) throw new Error('Failed to fetch scenarios');
    return res.json();
  },

  async processEmail(
    sender: string,
    body: string,
    subject?: string
  ): Promise<ProcessResponse> {
    const res = await fetch(`${API_BASE}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender, body, subject }),
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Request failed');
    }

    return res.json();
  },
};
```

### 3. Main Component
```tsx
// EmailProcessorDemo.tsx
import { useState, useEffect } from 'react';
import { api } from './api';
import type { ProcessResponse, DemoScenario } from './types';

export default function EmailProcessorDemo() {
  const [sender, setSender] = useState('john.doe@company.com');
  const [subject, setSubject] = useState('Document Request');
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ProcessResponse | null>(null);
  const [scenarios, setScenarios] = useState<DemoScenario[]>([]);

  useEffect(() => {
    api.getDemoScenarios().then(data => setScenarios(data.scenarios));
  }, []);

  const handleProcess = async () => {
    if (!sender || !body) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await api.processEmail(sender, body, subject);
      setResult(response);
    } catch (error) {
      console.error(error);
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const loadScenario = (scenario: DemoScenario) => {
    setSender(scenario.request.sender);
    setSubject(scenario.request.subject);
    setBody(scenario.request.body);
  };

  return (
    <div className="email-processor">
      {/* Left Panel - Input */}
      <div className="input-panel">
        <h2>📧 Email Request</h2>

        <label>From:</label>
        <select value={sender} onChange={e => setSender(e.target.value)}>
          <option value="john.doe@company.com">
            john.doe@company.com (Senior Engineer)
          </option>
          <option value="intern@company.com">
            intern@company.com (Intern)
          </option>
          <option value="cfo@company.com">
            cfo@company.com (CFO)
          </option>
        </select>

        <label>Subject:</label>
        <input
          type="text"
          value={subject}
          onChange={e => setSubject(e.target.value)}
          placeholder="Document Request"
        />

        <label>Body:</label>
        <textarea
          value={body}
          onChange={e => setBody(e.target.value)}
          placeholder="I need the API documentation..."
          rows={6}
        />

        <div className="quick-demos">
          <label>Quick Demos:</label>
          {scenarios.map(s => (
            <button
              key={s.id}
              onClick={() => loadScenario(s)}
              className="demo-btn"
            >
              {s.name}
            </button>
          ))}
        </div>

        <button
          onClick={handleProcess}
          disabled={loading || !sender || !body}
          className="process-btn"
        >
          {loading ? 'Processing...' : 'Process Request'}
        </button>
      </div>

      {/* Right Panel - Results */}
      <div className="results-panel">
        {loading && <div className="loading">Processing...</div>}

        {result && (
          <>
            {/* Agent Steps */}
            <div className="agent-steps">
              <h3>🔄 Agent Processing</h3>
              {result.agent_steps.map((step, i) => (
                <AgentStepCard key={i} step={step} />
              ))}
            </div>

            {/* Final Response */}
            <div className="email-response">
              <h3>✉️ Generated Response</h3>
              <EmailCard
                to={result.request.sender}
                subject={result.request.subject}
                body={result.final_response}
              />
            </div>

            {/* Document Preview */}
            {result.approved_document && (
              <div className="document-preview">
                <h3>📄 Approved Document</h3>
                <DocumentCard doc={result.approved_document} />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

// Agent Step Card Component
function AgentStepCard({ step }: { step: AgentStep }) {
  const isApproved = step.data.decision === 'approved';
  const isDenied = step.data.decision === 'denied';

  return (
    <div className="agent-card">
      <div className="agent-header">
        <span className="icon">{step.icon}</span>
        <span className="name">{step.agent}</span>
        <span className="status">✓ {step.status}</span>
      </div>

      <div className="agent-data">
        {step.agent === 'Doc Finder' && (
          <>
            <div>Query: "{step.data.search_query}"</div>
            <div>Found {step.data.documents_found} document(s)</div>
          </>
        )}

        {step.agent === 'Security Check' && (
          <>
            <div className={isApproved ? 'approved' : 'denied'}>
              Decision: {isApproved ? '✅ APPROVED' : '❌ DENIED'}
            </div>
            <div>Role: {step.data.user_role}</div>
            <div>Clearance: {step.data.user_clearance}</div>
            <div className="reasoning">{step.data.reasoning}</div>
          </>
        )}

        {step.agent === 'Response Generator' && (
          <div>Email crafted successfully</div>
        )}
      </div>
    </div>
  );
}

// Email Card Component
function EmailCard({ to, subject, body }: any) {
  return (
    <div className="email-card">
      <div className="email-header">
        <div><strong>To:</strong> {to}</div>
        <div><strong>Re:</strong> {subject}</div>
      </div>
      <div className="email-body">{body}</div>
    </div>
  );
}

// Document Card Component
function DocumentCard({ doc }: { doc: Document }) {
  return (
    <div className="document-card">
      <h4>{doc.name}</h4>
      <p>{doc.description}</p>
      <a href={doc.url} target="_blank" rel="noopener noreferrer">
        🔗 Open Document
      </a>
    </div>
  );
}
```

### 4. Styles (CSS)
```css
/* styles.css */
.email-processor {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  height: 100vh;
  padding: 24px;
  background: var(--background);
  font-family: 'Inter', sans-serif;
}

.input-panel,
.results-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-panel {
  background: var(--surface);
  padding: 24px;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.results-panel {
  overflow-y: auto;
}

/* Form Elements */
label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

input,
textarea,
select {
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

textarea {
  resize: vertical;
  min-height: 120px;
}

/* Buttons */
.process-btn {
  padding: 12px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.process-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.process-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.demo-btn {
  padding: 8px 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  transition: border-color 0.2s;
}

.demo-btn:hover {
  border-color: var(--accent);
}

/* Agent Cards */
.agent-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
}

.agent-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 600;
}

.agent-header .icon {
  font-size: 20px;
}

.agent-header .status {
  margin-left: auto;
  font-size: 12px;
  color: var(--success);
}

.agent-data {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.approved {
  color: var(--success);
  font-weight: 600;
}

.denied {
  color: var(--error);
  font-weight: 600;
}

.reasoning {
  font-style: italic;
  margin-top: 4px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 4px;
}

/* Email Card */
.email-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.email-header {
  padding-bottom: 12px;
  margin-bottom: 12px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}

.email-body {
  line-height: 1.6;
  white-space: pre-wrap;
}

/* Document Card */
.document-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
}

.document-card h4 {
  margin: 0 0 8px 0;
}

.document-card a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}

.document-card a:hover {
  text-decoration: underline;
}
```

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
# In your Lovable project
npm install
```

### Step 2: Add the Component
Create the files above in your Lovable project:
- `components/EmailProcessorDemo.tsx`
- `types/api.ts`
- `services/api.ts`
- `styles/email-processor.css`

### Step 3: Test the API
```bash
# Test the backend is running
curl https://web-production-5c5b4.up.railway.app/health

# Get demo scenarios
curl https://web-production-5c5b4.up.railway.app/demo-scenarios
```

### Step 4: Use the Component
```tsx
// In your app
import EmailProcessorDemo from './components/EmailProcessorDemo';

function App() {
  return <EmailProcessorDemo />;
}
```

---

## 🎯 Demo Flow

### Recommended Demo Order:

1. **Show the Interface**
   - Point out the 3 demo buttons
   - Explain the two-panel layout

2. **Run Scenario 1: ✅ Approved**
   - Click "✅ Approved Request"
   - Click "Process Request"
   - Watch agents process in real-time
   - Show the approved email response
   - Show the document link

3. **Run Scenario 2: ❌ Denied**
   - Click "❌ Denied Request"
   - Process it
   - Show how same document is denied for intern
   - Highlight the security reasoning

4. **Run Scenario 3: 🔐 Executive**
   - Show executive accessing financial data
   - Demonstrate clearance levels working

5. **Optional: Custom Input**
   - Type a custom request
   - Show it works with any input

---

## 📝 Notes

- **CORS is enabled** - Your Lovable frontend can call the Railway backend directly
- **Error handling** - API returns detailed error messages
- **Rate limiting** - Currently none, but consider adding for production
- **Authentication** - Not implemented (demo purposes)
- **Deployment** - Backend auto-deploys on Railway when you push to GitHub

---

## 🐛 Troubleshooting

### Issue: CORS errors
**Solution:** Backend has CORS enabled for all origins. Clear browser cache.

### Issue: API not responding
**Solution:** Check Railway deployment status at https://railway.app

### Issue: Slow responses
**Solution:** First request may be slow (cold start). Subsequent requests are fast.

### Issue: OpenAI errors
**Solution:** Verify `OPENAI_API_KEY` is set in Railway environment variables

---

## 📞 Support

Backend is live at: `https://web-production-5c5b4.up.railway.app`

Test it works:
```bash
curl https://web-production-5c5b4.up.railway.app/health
```

Expected: `{"status": "healthy"}`
