from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

SONATYPE_USER = os.getenv("SONATYPE_USER")
SONATYPE_TOKEN = os.getenv("SONATYPE_TOKEN")