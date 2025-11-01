from agents.doc_finder import find_documents
from agents.security import check_permissions
from agents.response_generator import generate_response
from data.mongodb import get_user_profile

def process_email(sender_email: str, subject: str, body: str) -> dict:
    """
    Main pipeline: orchestrates all 3 LLM agents
    Returns: dict with agent steps, final response, and metadata
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

    agent_steps = []

    # Step 1: Find relevant documents
    doc_info = find_documents(body)
    agent_steps.append(doc_info['step_info'])

    if not doc_info['documents']:
        print("\\n❌ No documents found")
        return {
            "success": False,
            "error": "No documents found",
            "agent_steps": agent_steps,
            "final_response": "I couldn't find the document you requested. Could you provide more details?",
            "approved_document": None
        }

    # Step 2: Check security/permissions
    user_profile = get_user_profile(sender_email)
    security_result = check_permissions(user_profile, doc_info)
    agent_steps.append(security_result['step_info'])

    # Step 3: Generate response
    response_data = generate_response(email_context, security_result, doc_info)
    agent_steps.append(response_data['step_info'])

    final_response = response_data['email_response']

    print("\\n" + "="*70)
    print("GENERATED EMAIL RESPONSE:")
    print("="*70)
    print(final_response)
    print("="*70)

    # Return structured data
    return {
        "success": True,
        "agent_steps": agent_steps,
        "final_response": final_response,
        "approved_document": response_data['selected_document'],
        "user_profile": {
            "name": user_profile.get('name'),
            "role": user_profile.get('role'),
            "clearance": user_profile.get('clearance')
        },
        "request": {
            "sender": sender_email,
            "subject": subject,
            "body": body
        }
    }