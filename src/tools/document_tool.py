import json
from google import genai
from google.genai import types
from src.env import GENAI_API_KEY

client = genai.Client(api_key=GENAI_API_KEY)


def summarize_document(text: str) -> str:
    if not text or not text.strip():
        return "No text provided for summarization."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a concise summarization assistant. "
                "Summarize the following content clearly, list key points, and provide any suggested actions."
            ),
            temperature=0.2
        )
    )
    return f"Document summary:\n{response.text}"
