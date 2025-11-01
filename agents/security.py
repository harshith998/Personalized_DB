import json
import re
from config import openai_client, OPENAI_MODEL, MAX_COMPLETION_TOKENS

def check_permissions(user_profile: dict, doc_info: dict) -> dict:
    """
    Determine if user has access to requested documents
    Returns: dict with approved (bool), reasoning (str), selected_doc (str), and step info
    """
    print("\\n🔒 [Agent 2: Security] Checking permissions...")

    prompt = f"""Determine if this user should have access to the requested documents.

USER PROFILE:
{json.dumps(user_profile, indent=2)}

REQUESTED DOCUMENTS:
{json.dumps(doc_info['documents'], indent=2)}

Rules:
- Match user clearance level with document required_clearance
- Consider role, department, and tenure

Respond with ONLY a JSON object:
{{"approved": true/false, "reasoning": "brief explanation", "selected_doc": "doc_id or null"}}"""

    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        max_completion_tokens=MAX_COMPLETION_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    llm_output = response.choices[0].message.content.strip()

    # Try to extract JSON if wrapped in markdown or extra text
    json_match = re.search(r'\\{.*\\}', llm_output, re.DOTALL)
    if json_match:
        llm_output = json_match.group(0)

    try:
        result = json.loads(llm_output)
    except json.JSONDecodeError as e:
        print(f"   ⚠️  JSON Parse Error. Raw output: {llm_output}")
        # Fallback to deny
        result = {
            "approved": False,
            "reasoning": "Unable to process security check",
            "selected_doc": None
        }

    status = "✅ APPROVED" if result.get('approved', False) else "❌ DENIED"
    print(f"   {status}")
    print(f"   Reasoning: {result.get('reasoning', 'N/A')}")

    # Add step info to result
    result['step_info'] = {
        "agent": "Security Check",
        "status": "complete",
        "icon": "🔒",
        "data": {
            "decision": "approved" if result.get('approved', False) else "denied",
            "reasoning": result.get('reasoning', 'N/A'),
            "user_clearance": user_profile.get('clearance', 'unknown'),
            "user_role": user_profile.get('role', 'unknown'),
            "selected_doc": result.get('selected_doc'),
            "llm_reasoning": llm_output
        }
    }

    return result