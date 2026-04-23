from dotenv import load_dotenv
load_dotenv()
from google import genai
import os
from config.settings import MODEL_NAME

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        # Safe extraction
        if hasattr(response, "text") and response.text:
            return response.text
        else:
            return str(response)

    except Exception as e:
        return f"Error: {str(e)}"