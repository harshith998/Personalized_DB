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
OPENAI_MODEL = "gpt-5"
MAX_TOKENS = 500
