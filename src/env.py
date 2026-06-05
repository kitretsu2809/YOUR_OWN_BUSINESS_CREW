import os
from pathlib import Path
import dotenv

# Load environment variables from the project .env file explicitly.
project_root = Path(__file__).resolve().parents[1]
dotenv_path = project_root / ".env"
print(dotenv_path)  # Debugging line to check if the .env path is correct
dotenv.load_dotenv(dotenv_path)

# Core API keys
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
USER_PRESET = os.getenv("USER_PRESET", "student")

# Optional integrations for future tools
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
CALENDAR_API_KEY = os.getenv("CALENDAR_API_KEY")


def require_env(name: str, value: str | None) -> str:
    if not value:
        raise EnvironmentError(f"Environment variable {name} is required but not set.")
    return value
