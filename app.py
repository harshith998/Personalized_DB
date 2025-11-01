from flask import Flask, request, jsonify
from pipeline import process_email
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Personalized Document Response System",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/process": "POST - Process email and generate response",
            "/health": "GET - Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/process', methods=['POST'])
def process():
    """
    Process an email and generate a response

    Expected JSON payload:
    {
        "sender": "user@example.com",
        "subject": "Request for document",
        "body": "I need the API documentation"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        sender = data.get('sender')
        subject = data.get('subject', 'Document Request')
        body = data.get('body')

        if not sender:
            return jsonify({"error": "sender field is required"}), 400

        if not body:
            return jsonify({"error": "body field is required"}), 400

        # Process the email through the pipeline
        response = process_email(sender, subject, body)

        return jsonify({
            "success": True,
            "response": response,
            "sender": sender,
            "subject": subject
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
