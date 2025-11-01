def search_documents(query: str) -> list:
    # Mock document database - replace with Supermemory API
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
    
    # Simple keyword matching - replace with semantic search
    query_lower = query.lower()
    results = []
    
    for doc in mock_docs:
        if (query_lower in doc['name'].lower() or 
            query_lower in doc['description'].lower()):
            results.append(doc)
    
    return results[:3]