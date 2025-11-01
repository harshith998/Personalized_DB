# GPT-5 Integration Guide

## ✅ Successfully Integrated OpenAI GPT-5

### Model Configuration
- **Model**: `gpt-5-mini` (cost-effective for demos)
- **Pricing**: $0.25/1M input tokens
- **Context**: 400K tokens
- **Max Output**: 128K tokens (we use 7000 for responses)

### Key API Changes from GPT-4

#### 1. Parameter Name Change
**Old (GPT-4):**
```python
openai_client.chat.completions.create(
    model="gpt-4",
    max_tokens=500,  # ❌ Old parameter
    messages=[...]
)
```

**New (GPT-5):**
```python
openai_client.chat.completions.create(
    model="gpt-5-mini",
    max_completion_tokens=7000,  # ✅ New parameter
    messages=[...]
)
```

### Model Options

| Model | Cost (Input/Output) | Use Case |
|-------|---------------------|----------|
| `gpt-5` | $1.25 / $10.00 per 1M | Production, highest quality |
| `gpt-5-mini` | $0.25 / TBD per 1M | **Demo/Development** (current) |
| `gpt-5-nano` | $0.05 / TBD per 1M | High-volume, simple tasks |

### Files Updated

1. **[config.py](config.py)** - Model config + max_completion_tokens
2. **[agents/doc_finder.py](agents/doc_finder.py)** - Import + API call
3. **[agents/security.py](agents/security.py)** - Import + API call
4. **[agents/response_generator.py](agents/response_generator.py)** - Import + API call

### Testing

**Local test:**
```bash
curl -X POST http://localhost:8080/process \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "john.doe@company.com",
    "body": "I need the API documentation"
  }'
```

**Production test (Railway):**
```bash
curl -X POST https://web-production-5c5b4.up.railway.app/process \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "john.doe@company.com",
    "body": "I need the API documentation"
  }'
```

### Reasoning Levels (Advanced)

GPT-5 supports reasoning levels: `minimal`, `low`, `medium`, `high`.

To use them via the **Responses API** (not Chat Completions):
```python
# Different endpoint for reasoning
response = openai_client.responses.create(
    model="gpt-5",
    input="Your prompt",
    reasoning={"summary": "auto"}  # or specify level
)
```

**Note:** We use the standard Chat Completions API for simplicity.

### Deployment

After updating to GPT-5, deploy to Railway:
```bash
git add .
git commit -m "Integrate GPT-5-mini with max_completion_tokens"
git push
```

Railway will auto-deploy. Ensure `OPENAI_API_KEY` is set in Railway environment variables.

### References

- [GPT-5 Official Docs](https://platform.openai.com/docs/models/gpt-5)
- [GPT-5 Announcement](https://openai.com/index/introducing-gpt-5-for-developers/)
- Model snapshot: `gpt-5-2025-08-07`

### Current Status

✅ GPT-5-mini integrated and tested
✅ All 3 agents working
✅ max_completion_tokens = 7000
✅ Ready for Railway deployment
