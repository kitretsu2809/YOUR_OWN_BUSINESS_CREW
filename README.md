# YOUR_OWN_BUSINESS_CREW
THE BUSINESS AUTOMATION

## Overview
This project is a customizable automation engine for students, founders, and content creators. It routes tasks through a CEO decision layer and department skills, then executes them with a generalized worker agent.

## What changed
- Added user presets for `personal`,`student`, `founder`, and `creator`
- Added department skills and allowed tools metadata
- Added a single configurable initialization flow via `main.py`
- Added a clean configuration schema in `config/schema.py`

## Usage
Run with a built-in preset:

```bash
python3 main.py --preset student --prompt "Create a study roadmap for AI internships."
```

Use a custom JSON config file:

```bash
python3 main.py --config path/to/config.json --prompt "Find me internship opportunities and draft outreach emails."
```

## Environment variables
Create a `.env` file in the project root from `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` and set your values.
At minimum, the current project requires:

```bash
GENAI_API_KEY=your_google_genai_api_key_here
```

Optional integrations include:

```bash
USER_PRESET=student
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email_user
SMTP_PASSWORD=your_email_password
EMAIL_FROM=you@example.com
GITHUB_TOKEN=your_github_token_here
SEARCH_API_KEY=your_search_api_key_here
CALENDAR_API_KEY=your_calendar_api_key_here
```

### GitHub token guidance
- For local development, use a **fine-grained personal access token** if possible.
- If you are using a GitHub App, generate a GitHub App installation token and store that as `GITHUB_TOKEN`.

### Search API support
- If `SEARCH_API_KEY` is configured, the app uses Bing Web Search.
- If not, it falls back to DuckDuckGo.

### Calendar API support
- `POST /calendar` returns an `.ics` event payload for the requested event.
- If `CALENDAR_API_KEY` is provided, the system retains the key for future hosted calendar provider integration.

The project loads `.env` automatically using the centralized `src/env.py` loader.

## API wrapper
A simple FastAPI wrapper is available in `api.py`.

Run the API server:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Default endpoints:
- `GET /health` — health check
- `POST /generate` — run a task through the engine
- `POST /email` — send an email via configured SMTP
- `POST /search` — run a web search on a query
- `POST /todo` — create a todo item- `POST /calendar` — generate an iCalendar event payload
- `GET /github/me` — validate the GitHub token and return the authenticated user- `POST /summarize` — summarize text content
- `POST /profile-audit` — audit a user profile and recommend improvements

Example API request:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Create a study roadmap for AI internships.","preset":"student"}'
```

Example frontend fetch call:

```javascript
async function generateTask(prompt, preset = 'student') {
  const response = await fetch('http://localhost:8000/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, preset })
  });
  if (!response.ok) {
    throw new Error('API request failed');
  }
  return response.json();
}

generateTask('Draft a cold email for AI internship outreach.', 'student')
  .then(result => console.log(result))
  .catch(console.error);
```

## General support fallback

The engine includes a `general_support` department that can be selected when a task is broad, open-ended, or cross-functional. This fallback department can leverage search, email sending, todo creation, calendar event generation, document summarization, and profile auditing to complete more complex requests.

## Direct tool endpoints

You can also call these tools directly if you want a single atomic action:
- `POST /summarize` — summarize long text
- `POST /profile-audit` — review a user profile and receive improvement suggestions

## Config presets
Built-in presets are defined in `config/presets.py` and include:
- `student`
- `founder`
- `creator`

Each preset defines active departments, focus areas, and skills for the user.

