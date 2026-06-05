import json
import re
from pathlib import Path
from typing import Optional, Dict
from src.tools.search_tool import web_search

CONTACTS_FILE = Path(__file__).resolve().parents[1] / "contacts.json"

# Simple contact cache loaded from disk
_contacts: Dict[str, str] = {}


def _load_contacts() -> None:
    global _contacts
    if CONTACTS_FILE.exists():
        try:
            with CONTACTS_FILE.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                if isinstance(data, dict):
                    _contacts = {k.lower(): v for k, v in data.items()}
        except Exception:
            _contacts = {}


def _save_contacts() -> None:
    CONTACTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CONTACTS_FILE.open("w", encoding="utf-8") as fh:
        json.dump(_contacts, fh, indent=2)


# Initialize cached contacts from disk
_load_contacts()


def add_contact(name: str, email: str) -> None:
    _contacts[name.lower()] = email
    _save_contacts()


def get_contact(name: str) -> Optional[str]:
    return _contacts.get(name.lower())


def _extract_email_from_text(text: str) -> Optional[str]:
    if not text:
        return None
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def find_email_by_name(name: str, max_search_results: int = 5) -> Optional[str]:
    """Try to resolve an email address for `name`.

    Strategy:
    - Check local cache
    - Use web search for "{name} email" and extract the first email-looking string
    """
    cached = get_contact(name)
    if cached:
        return cached

    query = f"{name} email"
    results = web_search(query, max_results=max_search_results)
    for item in results:
        # search in title, snippet, and url
        for field in (item.get("title", ""), item.get("snippet", ""), item.get("url", "")):
            email = _extract_email_from_text(field)
            if email:
                add_contact(name, email)
                return email
    return None
