import os
import json
import anthropic

# Initialize Anthropic client
claude = anthropic.Anthropic(api_key='key')

# ============================================================================
# PLACEHOLDER DATA SOURCES (Replace with real MongoDB + Supermemory)
# ============================================================================

def get_user_profile(email: str) -> dict:
    """
    Placeholder for MongoDB user lookup
    Returns user's role, department, clearance level
    """
    mock_users = {
        "john.doe@company.com": {
            "name": "John Doe",
            "role": "Senior Engineer",
            "department": "Engineering",
            "clearance": "standard",
            "tenure_months": 24
        },
        "intern@company.com": {
            "name": "Jane Intern",
            "role": "Software Intern",
            "department": "Engineering",
            "clearance": "limited",
            "tenure_months": 1
        },
        "cfo@company.com": {
            "name": "Alice CFO",
            "role": "Chief Financial Officer",
            "department": "Finance",
            "clearance": "executive",
            "tenure_months": 60
        }
    }
    
    return mock_users.get(email, {
        "name": "Unknown",
        "role": "External",
        "department": "None",
        "clearance": "none",
        "tenure_months": 0
    })

def search_supermemory(query: str) -> list:
    """
    Placeholder for Supermemory semantic search
    Returns list of documents with metadata
    """
    mock_docs = [
        {
            "id": "doc_001",
            "name": "Q4 2024 Financial Report",
            "url": "https://docs.google.com/document/d/abc123",
            "description": "Quarterly financial performance, revenue breakdown, and projections",
            "sensitivity": "confidential",
            "required_clearance": "executive"
        },
        {
            "id": "doc_002",
            "name": "API Documentation v2.1",
            "url": "https://docs.google.com/document/d/def456",
            "description": "REST API endpoints, authentication, and usage examples for internal services",
            "sensitivity": "internal",
            "required_clearance": "standard"
        },
        {
            "id": "doc_003",
            "name": "New Hire Onboarding Guide",
            "url": "https://docs.google.com/document/d/ghi789",
            "description": "Complete onboarding process, benefits info, and company policies",
            "sensitivity": "public",
            "required_clearance": "limited"
        },
        {
            "id": "doc_004",
            "name": "Engineering Playbook",
            "url": "https://docs.google.com/document/d/jkl012",
            "description": "Best practices, code review guidelines, and deployment procedures",
            "sensitivity": "internal",
            "required_clearance": "standard"
        }
    ]
    
    # Simple keyword matching (real version would use semantic embeddings)
    query_lower = query.lower()
    results = []
    
    for doc in mock_docs:
        if (query_lower in doc['name'].lower() or 
            query_lower in doc['description'].lower()):
            results.append(doc)
    
    return results[:3]  # Return top 3 matches

# ============================================================================
# 3-LLM PIPELINE
# ============================================================================

def doc_finder_llm(email_body: str) -> dict:
    """
    LLM Agent #1: Analyzes email and finds relevant documents
    """
    print("\n🔍 [Agent 1: Doc Finder] Analyzing request...")
    
    prompt = f"""You are a document retrieval assistant. Analyze this email and extract what document(s) the user is requesting.

Email body:
{email_body}

Output a JSON object with:
- "search_query": concise search query to find the document (2-5 words)
- "request_type": what they're asking for (e.g., "financial report", "documentation", "guide")

Only output valid JSON, nothing else."""

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    llm_output = response.content[0].text
    parsed = json.loads(llm_output)
    
    # Search Supermemory with extracted query
    search_query = parsed.get("search_query", email_body[:50])
    docs = search_supermemory(search_query)
    
    print(f"   Query: '{search_query}'")
    print(f"   Found {len(docs)} document(s)")
    
    return {
        "search_query": search_query,
        "request_type": parsed.get("request_type"),
        "documents": docs
    }

def security_llm(user_profile: dict, doc_info: dict) -> dict:
    """
    LLM Agent #2: Determines if user should have access
    """
    print("\n🔒 [Agent 2: Security] Checking permissions...")
    
    prompt = f"""You are a security agent that determines if a user should have access to requested documents.

USER PROFILE:
{json.dumps(user_profile, indent=2)}

REQUESTED DOCUMENTS:
{json.dumps(doc_info['documents'], indent=2)}

Analyze if this user should have access based on:
- Their role and clearance level
- Document sensitivity and required clearance
- Tenure and department
- Principle of least privilege

Output a JSON object with:
- "approved": true/false
- "reasoning": brief explanation (1-2 sentences)
- "selected_doc": if approved, which document to send (provide the doc id)

Only output valid JSON, nothing else."""

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    llm_output = response.content[0].text
    result = json.loads(llm_output)
    
    status = "✅ APPROVED" if result['approved'] else "❌ DENIED"
    print(f"   {status}")
    print(f"   Reasoning: {result['reasoning']}")
    
    return result

def response_generator_llm(email_context: dict, security_result: dict, doc_info: dict) -> str:
    """
    LLM Agent #3: Generates natural email response
    """
    print("\n✍️  [Agent 3: Response Generator] Crafting reply...")
    
    if security_result['approved']:
        # Find the selected document
        selected_doc = None
        for doc in doc_info['documents']:
            if doc['id'] == security_result.get('selected_doc'):
                selected_doc = doc
                break
        
        if not selected_doc and doc_info['documents']:
            selected_doc = doc_info['documents'][0]
        
        prompt = f"""Write a brief, professional email response providing the requested document.

ORIGINAL EMAIL:
From: {email_context['sender']}
Subject: {email_context['subject']}
Body: {email_context['body']}

DOCUMENT TO PROVIDE:
Name: {selected_doc['name']}
URL: {selected_doc['url']}
Description: {selected_doc['description']}

Write a helpful response that:
- Acknowledges their request
- Provides the document name and link
- Is warm but professional
- Keep it under 4 sentences

Do not include greeting or signature, just the body."""

    else:
        prompt = f"""Write a brief, professional email declining the document request.

ORIGINAL EMAIL:
From: {email_context['sender']}
Subject: {email_context['subject']}
Body: {email_context['body']}

DENIAL REASON:
{security_result['reasoning']}

Write a polite response that:
- Acknowledges their request
- Explains they don't have access (without being too specific about why)
- Suggests they contact their manager or IT if needed
- Keep it under 3 sentences

Do not include greeting or signature, just the body."""

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def process_email(sender_email: str, subject: str, body: str):
    """
    Main pipeline: runs 3 LLM agents in sequence
    """
    print("="*70)
    print(f"📨 Processing email from: {sender_email}")
    print(f"   Subject: {subject}")
    print("="*70)
    
    email_context = {
        'sender': sender_email,
        'subject': subject,
        'body': body
    }
    
    # Step 1: Find relevant documents
    doc_info = doc_finder_llm(body)
    
    if not doc_info['documents']:
        print("\n❌ No documents found")
        return "I couldn't find the document you requested. Could you provide more details?"
    
    # Step 2: Check security/permissions
    user_profile = get_user_profile(sender_email)
    security_result = security_llm(user_profile, doc_info)
    
    # Step 3: Generate response
    response = response_generator_llm(email_context, security_result, doc_info)
    
    print("\n" + "="*70)
    print("GENERATED EMAIL RESPONSE:")
    print("="*70)
    print(response)
    print("="*70)
    
    return response

# ============================================================================
# TERMINAL INTERFACE
# ============================================================================

def main():
    print("🤖 3-LLM Email Response System")
    print("="*70)
    print("Available test users:")
    print("  - john.doe@company.com (Senior Engineer, standard clearance)")
    print("  - intern@company.com (Intern, limited clearance)")
    print("  - cfo@company.com (CFO, executive clearance)")
    print("\nAvailable documents:")
    print("  - Q4 2024 Financial Report (executive only)")
    print("  - API Documentation v2.1 (standard clearance)")
    print("  - New Hire Onboarding Guide (limited clearance)")
    print("  - Engineering Playbook (standard clearance)")
    print("="*70)
    print()
    
    while True:
        print("\n" + "="*70)
        sender = input("From (email address): ").strip()
        
        if not sender:
            print("👋 Exiting...")
            break
        
        subject = input("Subject: ").strip()
        if not subject:
            subject = "Document Request"
        
        print("Body (press Enter twice to finish):")
        body_lines = []
        while True:
            line = input()
            if line == "":
                if body_lines and body_lines[-1] == "":
                    body_lines.pop()
                    break
            body_lines.append(line)
        
        body = "\n".join(body_lines)
        
        if not body:
            print("❌ Email body cannot be empty")
            continue
        
        # Process the email
        process_email(sender, subject, body)

if __name__ == "__main__":
    main()