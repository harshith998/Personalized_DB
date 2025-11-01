from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import process_email
import os

app = Flask(__name__)

# Enable CORS for all routes (allows Lovable frontend to call this API)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Personalized Document Response System",
        "description": "3-LLM Agent Pipeline for Secure Document Requests",
        "status": "running",
        "version": "2.0.0",
        "endpoints": {
            "/process": "POST - Process email and generate response with agent steps",
            "/demo-scenarios": "GET - Get pre-configured demo scenarios",
            "/health": "GET - Health check"
        },
        "agents": [
            "🔍 Doc Finder - Analyzes requests and finds documents",
            "🔒 Security Check - Verifies user permissions",
            "✍️ Response Generator - Crafts personalized email responses"
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/demo-scenarios', methods=['GET'])
def demo_scenarios():
    """
    Returns pre-configured demo scenarios for testing
    """
    scenarios = [
        {
            "id": "approved_standard",
            "name": "✅ Approved Request (Standard User)",
            "description": "Senior Engineer requests API documentation",
            "request": {
                "sender": "john.doe@company.com",
                "subject": "API Documentation Request",
                "body": "Hey, I need the API documentation for the new endpoints we're working with."
            },
            "expected_outcome": "Approved - User has standard clearance"
        },
        {
            "id": "denied_intern",
            "name": "❌ Denied Request (Insufficient Clearance)",
            "description": "Intern tries to access financial report",
            "request": {
                "sender": "intern@company.com",
                "subject": "Financial Report",
                "body": "Can I get the Q4 2024 financial report? I need it for my analysis project."
            },
            "expected_outcome": "Denied - Requires executive clearance"
        },
        {
            "id": "approved_executive",
            "name": "🔐 Approved Executive Access",
            "description": "CFO requests sensitive financial data",
            "request": {
                "sender": "cfo@company.com",
                "subject": "Q4 Financial Review",
                "body": "I need to review our quarterly financial performance and revenue breakdown."
            },
            "expected_outcome": "Approved - Executive has full access"
        }
    ]

    return jsonify({
        "scenarios": scenarios,
        "available_users": [
            {
                "email": "john.doe@company.com",
                "name": "John Doe",
                "role": "Senior Engineer",
                "clearance": "standard"
            },
            {
                "email": "intern@company.com",
                "name": "Jane Intern",
                "role": "Software Intern",
                "clearance": "limited"
            },
            {
                "email": "cfo@company.com",
                "name": "Alice CFO",
                "role": "Chief Financial Officer",
                "clearance": "executive"
            }
        ]
    }), 200

@app.route('/process', methods=['POST'])
def process():
    """
    Process an email and generate a response with full agent step visibility

    Expected JSON payload:
    {
        "sender": "user@example.com",
        "subject": "Request for document" (optional),
        "body": "I need the API documentation"
    }

    Returns:
    {
        "success": true,
        "agent_steps": [...],
        "final_response": "...",
        "approved_document": {...} or null,
        "user_profile": {...},
        "request": {...}
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400

        sender = data.get('sender')
        subject = data.get('subject', 'Document Request')
        body = data.get('body')

        if not sender:
            return jsonify({
                "success": False,
                "error": "sender field is required"
            }), 400

        if not body:
            return jsonify({
                "success": False,
                "error": "body field is required"
            }), 400

        # Process the email through the pipeline
        # This now returns structured data with agent steps
        result = process_email(sender, subject, body)

        return jsonify(result), 200

    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
