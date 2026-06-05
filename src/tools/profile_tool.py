import json
from google import genai
from google.genai import types
from src.env import GENAI_API_KEY

client = genai.Client(api_key=GENAI_API_KEY)


def audit_profile(profile: dict) -> str:
    if not profile:
        return "No profile information provided for audit."

    profile_text = json.dumps(profile, indent=2)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=profile_text,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an expert profile and resume reviewer. "
                "Analyze this user profile, identify strengths, suggest improvements, and recommend next steps."
            ),
            temperature=0.3
        )
    )
    return f"Profile audit:\n{response.text}"
