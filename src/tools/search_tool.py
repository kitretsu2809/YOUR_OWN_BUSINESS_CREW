import os
import requests
from typing import List, Dict
from src.env import SEARCH_API_KEY

BING_SEARCH_ENDPOINT = os.getenv("BING_SEARCH_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search")


def _duckduckgo_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results: List[Dict[str, str]] = []
    if data.get("AbstractText"):
        results.append({"title": "Abstract", "snippet": data["AbstractText"], "url": "https://duckduckgo.com/"})

    for topic in data.get("RelatedTopics", [])[:max_results]:
        if isinstance(topic, dict) and topic.get("Text"):
            results.append({"title": topic.get("Text", "Search result"), "snippet": topic.get("Text", ""), "url": topic.get("FirstURL", "")})
        elif isinstance(topic, list):
            for item in topic[:max_results]:
                if item.get("Text"):
                    results.append({"title": item.get("Text", "Search result"), "snippet": item.get("Text", ""), "url": item.get("FirstURL", "")})
    return results[:max_results]


def _bing_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    headers = {"Ocp-Apim-Subscription-Key": SEARCH_API_KEY}
    params = {
        "q": query,
        "count": max_results,
        "textDecorations": False,
        "textFormat": "Raw"
    }
    response = requests.get(BING_SEARCH_ENDPOINT, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results: List[Dict[str, str]] = []
    for item in data.get("webPages", {}).get("value", [])[:max_results]:
        results.append({"title": item.get("name", "Search result"), "snippet": item.get("snippet", ""), "url": item.get("url", "")})
    return results


def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    if SEARCH_API_KEY:
        try:
            return _bing_search(query, max_results)
        except Exception:
            return _duckduckgo_search(query, max_results)
    return _duckduckgo_search(query, max_results)
