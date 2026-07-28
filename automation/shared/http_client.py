"""
HTTP client utilities for live deployment testing.
All requests target BASE_URL — never localhost.
"""

import os
import time
from typing import Optional

import requests

BASE_URL = os.environ.get(
    "BASE_URL",
    "https://viswanathsaisandeep.github.io/MediRoute/",
)
if not BASE_URL.endswith("/"):
    BASE_URL += "/"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "MediRoute-Automation/1.0"})


def get_url(path: str = "") -> str:
    """Build absolute URL from BASE_URL and path."""
    return BASE_URL.rstrip("/") + "/" + path.lstrip("/")


def fetch(path: str = "", timeout: int = 30) -> requests.Response:
    """GET request against live deployment."""
    return SESSION.get(get_url(path), timeout=timeout, allow_redirects=True)


def fetch_route(route: str, timeout: int = 30) -> requests.Response:
    """GET a hash-based Flutter route."""
    clean = route if route.startswith("/") else f"/{route}"
    return fetch(f"#{clean}", timeout=timeout)


def measure_response_time(path: str = "", timeout: int = 30) -> tuple[float, int, int]:
    """Return (elapsed_seconds, status_code, content_length)."""
    start = time.perf_counter()
    resp = fetch(path, timeout=timeout)
    elapsed = time.perf_counter() - start
    return elapsed, resp.status_code, len(resp.content)
