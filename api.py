from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, ValidationError
from typing import Any, Dict, List, Optional
from main import app as workflow_app, build_initial_state, load_profile
from src.tools.email_tool import send_email
from src.tools.search_tool import web_search
from src.tools.todo_tool import todo_manager
from src.tools.document_tool import summarize_document
from src.tools.profile_tool import audit_profile
from src.tools.calendar_tool import create_event
from src.tools.github_tool import get_authenticated_user
from src.tools.contact_tool import find_email_by_name
from src.tools.contact_tool import add_contact, get_contact

app = FastAPI(
    title="YOUR_OWN_BUSINESS_CREW API",
    description="A lightweight API wrapper for the business automation engine.",
    version="0.1.0"
)


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="The user task or request to automate.")
    preset: Optional[str] = Field(None, description="Optional built-in preset: student, founder, creator.")
    config: Optional[Dict[str, Any]] = Field(None, description="Optional custom configuration object.")


class GenerateResponse(BaseModel):
    prompt: str
    preset: Optional[str]
    events: List[Dict[str, Any]]
    final_messages: List[Dict[str, Any]]


class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str


class SearchRequest(BaseModel):
    query: str


class TodoRequest(BaseModel):
    title: str
    due: Optional[str] = Field(None, description="Optional due date for the todo.")


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text content to summarize.")


class ProfileAuditRequest(BaseModel):
    user_profile: Dict[str, Any] = Field(..., description="User profile data for audit.")


class CalendarEventRequest(BaseModel):
    title: str
    start_timestamp: str
    duration_minutes: Optional[int] = Field(60, description="Event duration in minutes.")
    description: Optional[str] = Field(None, description="Optional event description.")


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must not be empty.")

    try:
        profile = load_profile(preset=req.preset, raw_config=req.config)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid config: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to load profile: {exc}")

    initial_state = build_initial_state(profile, req.prompt)

    events: List[Dict[str, Any]] = []
    for event in workflow_app.stream(initial_state):
        events.append(event)

    final_messages = []
    for event in reversed(events):
        state_data = event.get("dynamic_worker") or event.get("ceo")
        if state_data and state_data.get("messages"):
            final_messages = state_data["messages"]
            break

    return GenerateResponse(
        prompt=req.prompt,
        preset=req.preset,
        events=events,
        final_messages=final_messages
    )


@app.post("/email")
def email(request: EmailRequest) -> Dict[str, str]:
    try:
        result = send_email(request.to, request.subject, request.body)
        return {"status": "sent", "message": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email send failed: {exc}")


@app.post("/search")
def search(request: SearchRequest) -> Dict[str, Any]:
    try:
        results = web_search(request.query)
        return {"status": "ok", "results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Search failed: {exc}")


@app.post("/todo")
def create_todo(request: TodoRequest) -> Dict[str, Any]:
    try:
        todo = todo_manager.add_task(request.title, due=request.due)
        return {"status": "created", "todo": todo}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Todo creation failed: {exc}")


@app.post("/calendar")
def create_calendar(request: CalendarEventRequest) -> Dict[str, str]:
    try:
        ics = create_event(request.title, request.start_timestamp, request.duration_minutes or 60, request.description)
        return {"status": "ok", "ics": ics}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Calendar event generation failed: {exc}")


@app.get("/github/me")
def github_me() -> Dict[str, Any]:
    try:
        profile = get_authenticated_user()
        return {"status": "ok", "profile": profile}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"GitHub token validation failed: {exc}")


@app.post("/summarize")
def summarize(request: SummarizeRequest) -> Dict[str, str]:
    try:
        summary = summarize_document(request.text)
        return {"status": "ok", "summary": summary}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {exc}")


@app.post("/profile-audit")
def profile_audit(request: ProfileAuditRequest) -> Dict[str, str]:
    try:
        audit = audit_profile(request.user_profile)
        return {"status": "ok", "audit": audit}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Profile audit failed: {exc}")


@app.get("/presets")
def list_presets() -> Dict[str, List[str]]:
    return {"presets": ["student", "founder", "creator"]}


class EmailByNameRequest(BaseModel):
    name: str
    subject: str
    body: str


@app.post("/email/by-name")
def email_by_name(request: EmailByNameRequest) -> Dict[str, Any]:
    try:
        email = find_email_by_name(request.name)
        if not email:
            raise HTTPException(status_code=404, detail=f"Could not resolve email for {request.name}")
        result = send_email(email, request.subject, request.body)
        return {"status": "sent", "to": email, "message": result}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email by name failed: {exc}")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


class ContactAddRequest(BaseModel):
    name: str
    email: EmailStr


@app.post("/contacts")
def add_contact_endpoint(request: ContactAddRequest) -> Dict[str, Any]:
    try:
        add_contact(request.name, request.email)
        return {"status": "added", "name": request.name, "email": request.email}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Add contact failed: {exc}")


@app.get("/contacts/{name}")
def get_contact_endpoint(name: str) -> Dict[str, Any]:
    try:
        email = get_contact(name)
        if not email:
            raise HTTPException(status_code=404, detail=f"Contact not found: {name}")
        return {"status": "ok", "name": name, "email": email}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Get contact failed: {exc}")
