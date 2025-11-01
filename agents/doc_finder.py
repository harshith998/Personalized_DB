import json
import re
from config import openai_client, OPENAI_MODEL, MAX_TOKENS
from data.supermemory import search_documents

def find_documents(email_body: str) -> dict:
    """
    Analyze email and find relevant documents
    Returns: dict with search_query, request_type, and documents list
    """
    print("\\n🔍 [Agent 1: Doc Finder] Analyzing request...")
    
    prompt = f"""Analyze this email and extract what document the user is requesting.

Email body:
{email_body}

Respond with ONLY a JSON object in this exact format:
{{"search_query": "2-5 word search term", "request_type": "type of document"}}

Example: {{"search_query": "financial report", "request_type": "quarterly report"}}"""

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    llm_output = response.choices[0].message.content.strip()
    
    # Try to extract JSON if wrapped in markdown or extra text
    json_match = re.search(r'\\{.*\\}', llm_output, re.DOTALL)
    if json_match:
        llm_output = json_match.group(0)
    
    try:
        parsed = json.loads(llm_output)
    except json.JSONDecodeError as e:
        print(f"   ⚠️  JSON Parse Error. Raw output: {llm_output}")
        # Fallback: extract keywords from email
        parsed = {
            "search_query": email_body[:50],
            "request_type": "document"
        }
    
    # Search documents using extracted query
    search_query = parsed.get("search_query", email_body[:50])
    docs = search_documents(search_query)
    
    print(f"   Query: '{search_query}'")
    print(f"   Found {len(docs)} document(s)")
    
    return {
        "search_query": search_query,
        "request_type": parsed.get("request_type"),
        "documents": docs
    }