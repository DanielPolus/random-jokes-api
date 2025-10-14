import httpx
from typing import Any, Dict, List
from fastapi import HTTPException
from httpx import RequestError

BASE_URL = "https://official-joke-api.appspot.com"
TIMEOUT = 5
MAX_N = 50

def get_random(path: str):
    url = BASE_URL + path
    try:
        resp = httpx.get(url, timeout=TIMEOUT)
    except RequestError:
        raise HTTPException(504, "No answer from the server")
    if resp.status_code != 200:
        raise HTTPException(502, "Something went wrong")

    try:
        data = resp.json()
    except ValueError:
        raise HTTPException(502, "Invalid json body")

    if data.get("id") and data.get("type") and data.get("setup") and data.get("punchline"):
        return data


def get_random_jokes(path: str):
    url = BASE_URL + path
    try:
        resp = httpx.get(url, timeout=TIMEOUT)
    except RequestError:
        raise HTTPException(504, "No answer from the server")
    if resp.status_code != 200:
        raise HTTPException(502, "Something went wrong")

    try:
        data = resp.json()
    except ValueError:
        raise HTTPException(502, "Invalid json body")

    if isinstance(data, List):
        note = None
        if len(data) != 10:
            note = f"Expected 10, got {len(data)}"
        return {"count": len(data), "items": data, "note": note}
