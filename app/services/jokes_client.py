import httpx
from typing import Any, Dict
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

    if isinstance(data, list):
        note = None
        if len(data) != 10:
            note = f"Expected 10, got {len(data)}"
        return {"count": len(data), "items": data, "note": note}

def get_random_n(n: int):
    if n > MAX_N or n < 1:
        raise HTTPException(400, "N must be between 1 and 50")
    url = f"{BASE_URL}/jokes/random/{n}"
    try:
        resp = httpx.get(url, timeout=TIMEOUT)
    except RequestError:
        HTTPException(504, "No answer from the server")

    if resp.status_code != 200:
        raise HTTPException(502, "Something went wrong")

    try:
        data = resp.json()
    except ValueError:
        raise HTTPException(502, "Invalid json body")

    if isinstance(data, list):
        note = None
        if len(data) != n:
            note = f"Expected {n}, got {len(data)}"
        return {"count": len(data), "items": data, "note": note}
    raise HTTPException(502, "Upstream returned non-list")

def get_type_random(joke_type: str):
    url = f"{BASE_URL}/jokes/{joke_type}/random"
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

    if isinstance(data, list):
        if len(data) == 0:
            raise HTTPException(404, "No jokes of such type found")
        item = data[0]
        if item.get("id") and item.get("type") and item.get("setup") and item.get("punchline"):
            return item

    raise HTTPException(502, "Something went wrong with isinstance")

def get_by_id(id: int):
    if id < 1:
        raise HTTPException(400, "id must be >= 1")

    url = f"{BASE_URL}/jokes/{id}"
    try:
        resp = httpx.get(url, timeout=TIMEOUT)
    except RequestError:
        raise HTTPException(504, "No answer from the server")

    if resp.status_code == 404:
        raise HTTPException(404, "Joke not found")

    if resp.status_code != 200:
        raise HTTPException(502, "Something went wrong")

    try:
        data = resp.json()
    except ValueError:
        raise HTTPException(502, "Invalid json body")

    if data.get("id") and data.get("type") and data.get("setup") and data.get("punchline"):
        return data
    raise HTTPException(502, "Upstream payload missing required fields")
