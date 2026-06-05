import json
from google import genai
from google.genai import types
from src.env import GENAI_API_KEY
from src.state import CorporateState
from typing import Dict, Any

client = genai.Client(api_key=GENAI_API_KEY)

def run_ceo(state: CorporateState) -> Dict[str, Any]:
    """
    Dynamically routes tasks based on the active departments and configured skills.
    """
    profile = state["business_profile"]
    user_profile = profile.get("user_profile", {})
    active_depts = profile.get("active_departments", [])
    available_names = [dept["name"] for dept in active_depts]

    # 1. Dynamically build the list of available departments for the AI prompt
    dept_descriptions = []
    for dept in active_depts:
        skills = dept.get("skills", [])
        skill_list = f" Skills: {', '.join(skills)}." if skills else ""
        dept_descriptions.append(
            f"- '{dept['name']}': Focuses on {', '.join(dept['focus_areas'])}.{skill_list}"
        )
    dept_descriptions = "\n".join(dept_descriptions)

    company_name = profile.get("company_name") or profile.get("organization_name") or user_profile.get("name", "User")
    industry = profile.get("industry") or user_profile.get("specialization") or "general work"
    audience = profile.get("target_audience") or "relevant stakeholders"
    tone = profile.get("brand_tone") or user_profile.get("preferred_tone") or "professional"
    objective = user_profile.get("objective", "Complete the requested task")

    # 2. Construct the dynamic executive prompt
    system_instruction = f"""You are the CEO of {company_name}, operating in the {industry} space.
    User Role: {user_profile.get('role', 'User')}.
    Objective: {objective}.
    Target Audience: {audience}.
    Brand Tone: {tone}.

    You have the following departments actively online and ready to execute tasks:
    {dept_descriptions}

    Review the task and the conversation history. Decide which single department needs to act next to best complete the user's request.
    If the task is broad, cross-functional, or unclear, choose 'general_support' as the fallback department.
    If the user's goal is already complete, respond with exactly 'finish'.

    CRITICAL: You must return output EXACTLY as a JSON object matching this structure:
    {{
        "reasoning": "Brief explanation of why this department was chosen",
        "next_department": "<exact_department_name_or_finish>"
    }}
    """

    # Build conversation context from message history
    conversation_context = ""
    for message in state.get("messages", []):
        if "role" in message and "parts" in message:
            role = message["role"].upper()
            text_parts = [str(part) if part is not None else "" for part in message.get("parts", [])]
            text = " ".join(text_parts).strip()
            conversation_context += f"{role}: {text}\n"
        else:
            conversation_context += str(message) + "\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_context,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    routing_target = "finish"
    try:
        decision = json.loads(response.text)
        candidate = decision.get("next_department", "finish")
        if candidate in available_names or candidate == "finish":
            routing_target = candidate
        elif "general_support" in available_names:
            routing_target = "general_support"
        else:
            # fallback if the agent chooses something else
            routing_target = available_names[0] if available_names else "finish"
    except Exception:
        if "general_support" in available_names:
            routing_target = "general_support"
        else:
            routing_target = available_names[0] if available_names else "finish"

    return {
        "next_action": routing_target,
        "task_complete": routing_target == "finish"
    }