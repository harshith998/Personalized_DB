import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API setup - load from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Model configuration
# GPT-5 options: "gpt-5" ($1.25/$10), "gpt-5-mini" ($0.25/input), "gpt-5-nano" ($0.05/input)
# Using gpt-5-mini for cost-effective demo (400K context, 128K max output)
OPENAI_MODEL = "gpt-5-mini"
MAX_COMPLETION_TOKENS = 7000  # GPT-5 max_completion_tokens (high limit for detailed responses)
