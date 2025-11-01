import os
from anthropic import Anthropic

# Anthropic API setup
ANTHROPIC_API_KEY = 'key'
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

claude_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Model configuration
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 500