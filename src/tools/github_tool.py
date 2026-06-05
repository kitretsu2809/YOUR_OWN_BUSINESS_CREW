import requests
from typing import Any, Dict, List, Optional
from src.env import GITHUB_TOKEN, require_env

def _github_headers() -> Dict[str, str]:
    token = require_env("GITHUB_TOKEN", GITHUB_TOKEN)
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }


def get_authenticated_user() -> Dict[str, Any]:
    print(GITHUB_TOKEN)  # Debugging line to check if the token is loaded
    url = "https://api.github.com/user"
    response = requests.get(url, headers=_github_headers(), timeout=10)
    response.raise_for_status()
    return response.json()


def list_repositories(visibility: str = "all", affiliation: str = "owner,collaborator", per_page: int = 50) -> List[Dict[str, Any]]:
    url = "https://api.github.com/user/repos"
    params = {
        "visibility": visibility,
        "affiliation": affiliation,
        "per_page": per_page
    }
    response = requests.get(url, headers=_github_headers(), params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def get_repository(owner: str, repo: str) -> Dict[str, Any]:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=_github_headers(), timeout=10)
    response.raise_for_status()
    return response.json()


def create_issue(owner: str, repo: str, title: str, body: Optional[str] = None) -> Dict[str, Any]:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    payload: Dict[str, Any] = {"title": title}
    if body:
        payload["body"] = body
    response = requests.post(url, headers=_github_headers(), json=payload, timeout=10)
    response.raise_for_status()
    return response.json()
