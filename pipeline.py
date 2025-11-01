from agents.doc_finder import find_documents
from agents.security import check_permissions
from agents.response_generator import generate_response
from data.mongodb import get_user_profile

def process_email(sender_email: str, subject: str, body: str) -> str:
    """
    Main pipeline: orchestrates all 3 LLM agents
    Returns: generated email response
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
    doc_info = find_documents(body)
    
    if not doc_info['documents']:
        print("\\n❌ No documents found")
        return "I couldn't find the document you requested. Could you provide more details?"
    
    # Step 2: Check security/permissions
    user_profile = get_user_profile(sender_email)
    security_result = check_permissions(user_profile, doc_info)
    
    # Step 3: Generate response
    response = generate_response(email_context, security_result, doc_info)
    
    print("\\n" + "="*70)
    print("GENERATED EMAIL RESPONSE:")
    print("="*70)
    print(response)
    print("="*70)
    
    return response