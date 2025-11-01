def get_user_profile(email: str) -> dict:
    # Mock database - replace with real MongoDB query
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