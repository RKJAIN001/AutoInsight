from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
else:
    print("API key loaded successfully (starts with):", api_key[:8] + "...")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Say hello in one short sentence."
    )

    print()
    print("Gemini responded:")
    print(response.text)