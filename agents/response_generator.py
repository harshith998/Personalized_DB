from config import openai_client, OPENAI_MODEL, MAX_TOKENS

def generate_response(email_context: dict, security_result: dict, doc_info: dict) -> str:
    """
    Generate natural email response
    Returns: string with email body
    """
    print("\\n✍️  [Agent 3: Response Generator] Crafting reply...")
    
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

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content