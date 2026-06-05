import json
import re
from google import genai
from google.genai import types
from src.env import GENAI_API_KEY
from src.state import CorporateState
from src.tools import create_event, send_email, todo_manager, web_search, summarize_document, audit_profile, find_email_by_name
from typing import Dict, Any, List, Optional

client = genai.Client(api_key=GENAI_API_KEY)


def _extract_email(text: str) -> Optional[str]:
    if not text:
        return None
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def _extract_subject(text: str) -> str:
    if not text:
        return "Automated message"
    match = re.search(r"subject[:\-]\s*(.+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip().split(".")[0][:80] or "Automated message"


def _extract_name_from_text(text: str) -> Optional[str]:
    if not text:
        return None
    # common patterns: "to NAME", "send to NAME", "for NAME"
    match = re.search(r"(?:to|for|send to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})", text)
    if match:
        return match.group(1).strip()
    # fallback: look for two capitalized words
    match = re.search(r"([A-Z][a-z]+\s+[A-Z][a-z]+)", text)
    if match:
        return match.group(1).strip()
    return None



def _parse_composed_email(text: str) -> (Optional[str], str):
    """Extract a subject and body from a composed email in free text.

    This parser handles markdown/bullet output and returns only the actual
    composed subject and body, not the surrounding action summary.
    """
    if not text:
        return None, ""

    normalized = text.replace('\r\n', '\n')

    subject = None
    subject_match = re.search(
        r'(?i)(?:\*\*|\*|__)?\s*subject\s*[:\-]\s*["“\']?(?P<subject>[^"”\']+?)["”\']?(?=\s*$|\n)',
        normalized
    )
    if subject_match:
        subject = subject_match.group('subject').strip()

    body = None
    # Prefer quoted body text after Body:
    body_match = re.search(
        r'(?i)\bbody\b\s*[:\-]\s*["“](?P<body>.*?)["”](?=\s*$|\n|\r|\n\s*\d+\.|\n\s*[\*\-])',
        normalized,
        flags=re.S
    )
    if body_match:
        body = body_match.group('body').strip()
    else:
        # Fallback to the section after Body: until the next numbered/bullet section
        body_match = re.search(
            r'(?i)\bbody\b\s*[:\-]\s*(?P<body>.*?)(?=\n\s*\d+\.|\n\s*[\*\-]|\n\[|$)',
            normalized,
            flags=re.S
        )
        if body_match:
            body = body_match.group('body').strip()
        else:
            parts = normalized.split('\n\n', 1)
            if len(parts) > 1:
                body = parts[1].strip()

    if not body:
        body = normalized.strip()

    if subject:
        subject = re.sub(r"^\*+\s*", "", subject)
        subject = re.sub(r"['\"”“]$", "", subject).replace('**', '').replace('*', '').strip()

    body = body.strip()
    body = re.sub(r"^\*+\s*", "", body, flags=re.MULTILINE)
    body = re.sub(r'\n\s*\d+\.\s.*$', '', body, flags=re.S)
    body = re.split(r'\[COMMUNICATION OUTPUT\]|\[COMMUNICATION OUTPUT\]', body, maxsplit=1)[0].strip()
    if body.startswith('"') and body.endswith('"'):
        body = body[1:-1].strip()
    if body.startswith("'") and body.endswith("'"):
        body = body[1:-1].strip()

    body = '\n\n'.join([p.strip() for p in body.split('\n\n') if p.strip()])

    return subject, body


def _format_search_results(results: List[Dict[str, str]]) -> str:
    if not results:
        return "No search results were found."
    lines = ["Search results:"]
    for idx, item in enumerate(results, start=1):
        title = item.get("title", "Result")
        snippet = item.get("snippet", "")
        url = item.get("url", "")
        lines.append(f"{idx}. {title} - {snippet} {url}".strip())
    return "\n".join(lines)


def _detect_email_intent(text: str) -> bool:
    normalized = text.lower()
    if "email" in normalized:
        return True
    if "send" in normalized and any(keyword in normalized for keyword in ["message", "mail", "note", "recipient", "contact"]):
        return True
    if "outreach" in normalized or "contact" in normalized:
        return True
    return False


def _is_direct_email_reference(text: str, email: str) -> bool:
    normalized = text.lower()
    candidate = email.lower()
    patterns = [
        rf"\bto\s+{re.escape(candidate)}\b",
        rf"\bsent\s+to\s+{re.escape(candidate)}\b",
        rf"\brecipient\b.*{re.escape(candidate)}",
        rf"\bsend\s+to\s+{re.escape(candidate)}\b",
        rf"\b{re.escape(candidate)}\b"
    ]
    return any(re.search(pattern, normalized) for pattern in patterns)


def _should_use_tool(text: str, keywords: List[str]) -> bool:
    normalized = text.lower()
    return any(keyword in normalized for keyword in keywords)


def _maybe_run_tools(state: CorporateState, department_name: str, response_text: str, tools: List[str]) -> tuple[List[str], bool]:
    messages: List[str] = []
    task_complete = False
    current_task = state.get("current_task", "")
    combined_text = f"{current_task}\n{response_text}"

    if any(tool in tools for tool in ["web_search"]) and _should_use_tool(combined_text, ["find", "search", "discover", "research", "opportunity", "internship", "market", "competitor"]):
        try:
            results = web_search(current_task or response_text)
            messages.append(_format_search_results(results))
        except Exception as exc:
            messages.append(f"Search tool failed: {exc}")

    if any(tool in tools for tool in ["email_sender", "email_composer"]) and _detect_email_intent(combined_text):
        to_address = _extract_email(current_task)
        name = None
        if not to_address:
            name = _extract_name_from_text(current_task) or _extract_name_from_text(response_text)
            if name:
                try:
                    found = find_email_by_name(name)
                    if found:
                        to_address = found
                        messages.append(f"Resolved {name} -> {to_address}")
                    else:
                        messages.append(f"Could not resolve an email address for recipient '{name}'. No email was sent.")
                except Exception as exc:
                    messages.append(f"Contact resolver failed: {exc}")

        if not to_address:
            response_email = _extract_email(response_text)
            if response_email and _is_direct_email_reference(response_text, response_email):
                to_address = response_email

        if to_address:
            parsed_subject, parsed_body = _parse_composed_email(response_text)
            if not parsed_body:
                messages.append("Could not extract a composed email body from the assistant response; email was not sent.")
            else:
                subject = parsed_subject or _extract_subject(current_task or response_text)
                body = parsed_body
                try:
                    result = send_email(to_address, subject, body)
                    messages.append(result)
                    task_complete = True
                except Exception as exc:
                    messages.append(f"Email tool failed: {exc}")
        else:
            messages.append("No valid recipient email was found or resolved; email was not sent.")

    if any(tool in tools for tool in ["calendar", "content_calendar"]) and _should_use_tool(combined_text, ["schedule", "meeting", "calendar", "reserve", "book", "plan", "event"]):
        try:
            start_timestamp = state.get("calendar_start") or state.get("current_task") or "2025-01-01T09:00:00"
            event_text = create_event(
                title=f"{department_name.title()} Task",
                start_timestamp=start_timestamp,
                duration_minutes=60,
                description=response_text
            )
            messages.append(f"Generated calendar event:\n{event_text}")
        except Exception as exc:
            messages.append(f"Calendar tool failed: {exc}")

    if any(tool in tools for tool in ["todo_manager"]) and _should_use_tool(combined_text, ["task", "todo", "action item", "next step", "follow up", "reminder"]):
        try:
            todo = todo_manager.add_task(current_task or response_text)
            messages.append(f"Created todo task: {todo['title']} (due: {todo.get('due')})")
        except Exception as exc:
            messages.append(f"Todo tool failed: {exc}")

    if "document_summarizer" in tools and _should_use_tool(combined_text, ["summarize", "summary", "digest", "key points"]):
        try:
            summary = summarize_document(current_task or response_text)
            messages.append(summary)
        except Exception as exc:
            messages.append(f"Document summarizer failed: {exc}")

    if "profile_audit" in tools and _should_use_tool(combined_text, ["profile", "resume", "cv", "portfolio", "bio"]):
        try:
            profile = state.get("business_profile", {}).get("user_profile", {})
            audit = audit_profile(profile)
            messages.append(audit)
        except Exception as exc:
            messages.append(f"Profile audit failed: {exc}")

    return messages, task_complete
def run_generalized_worker(state: CorporateState, department_name: str) -> Dict[str, Any]:
    """
    A unified, polymorphic agent node. It dynamically configures its system persona
    based on the department name passed to it by the graph topology.
    """
    profile = state["business_profile"]
    user_profile = profile.get("user_profile", {})
    company_name = profile.get("company_name") or profile.get("organization_name") or user_profile.get("name", "User")
    audience = profile.get("target_audience") or "relevant stakeholders"
    tone = profile.get("brand_tone") or user_profile.get("preferred_tone") or "professional"

    dept_config = next(
        (d for d in profile.get("active_departments", []) if d["name"] == department_name),
        {"focus_areas": ["General Execution"], "skills": [], "allowed_tools": []}
    )

    skills = dept_config.get("skills", [])
    skill_description = f"Use the following skills if they are appropriate: {', '.join(skills)}." if skills else ""
    tools = dept_config.get("allowed_tools", [])
    tool_description = f"Allowed tools: {', '.join(tools)}." if tools else ""

    system_instruction = f"""You are the Head of the '{department_name.upper()}' Department at {company_name}.
    Your user persona: {user_profile.get('role', 'laptop user')} with specialization in {user_profile.get('specialization', 'general work')}.
    Objective: {user_profile.get('objective', 'Respond to the user task carefully')}.
    Target Audience: {audience}.
    Brand Tone: {tone}.

    Your specific operational focus areas are: {', '.join(dept_config.get('focus_areas', []))}.
    {skill_description}
    {tool_description}

    Review the request and the existing work from other departments. Execute your department's specific portion of the task thoroughly.
    When you finish, summarize your output clearly and prefix it with [{department_name.upper()} OUTPUT].
    """

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
            temperature=0.5
        )
    )

    updated_messages = list(state.get("messages", [])) + [
        {"role": "model", "parts": [response.text]}
    ]

    tool_outputs, tool_task_complete = _maybe_run_tools(state, department_name, response.text, tools)
    for tool_output in tool_outputs:
        updated_messages.append({"role": "tool", "parts": [tool_output]})

    return {
        "messages": updated_messages,
        "next_action": "ceo",
        "task_complete": tool_task_complete
    }