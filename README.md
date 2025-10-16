# 🎭 Random Joke API
FastAPI proxy over Official Joke API with normalized responses, simple validation, and clean error handling.

Live demo: local only (dev) Docs: http://127.0.0.1:8000/docs

# 🚀 Tech Stack
Backend
FastAPI — lightweight web framework
httpx — HTTP client
Pydantic — response models & docs
Uvicorn — ASGI server
Testing
pytest — test runner
respx — mock httpx calls (no real network)

# ✨ Features
/jokes/random/ — one random joke (consistent object shape)

/jokes/ten/ — exactly 10 jokes (wrapped with count/items

/jokes/random/{n} — N random jokes with input validation (1..50)

/jokes/type/{joke_type}/random — normalizes provider’s list[1] → single object

/jokes/{id} — fetch by ID with proper 404 passthrough

Uniform JSON errors: 400/404/502/504

# ⚙️ Local Setup
## 1️⃣ Create & activate a virtual env (Windows PowerShell shown)
python -m venv venv .\venv\Scripts\Activate.ps1

## 2️⃣ Install deps
pip install -r requirements.txt

## 3️⃣ Run
uvicorn app.main:app --reload

## 4️⃣ Open
http://127.0.0.1:8000/docs

# 🗝️ API Endpoints
Method Endpoint Description Response

GET /health/ Health check {"status":"ok"}

GET /jokes/random/ One random joke Joke

GET /jokes/ten/ Ten jokes JokesList

GET /jokes/random/{n} N random jokes (1..50) JokesList

GET /jokes/type/{joke_type}/random Random joke by type (normalized) Joke

GET /jokes/{id} Joke by ID Joke

Joke {"id":1,"type":"programming","setup":"…","punchline":"…"}

JokesList {"count":10,"items":[{Joke}, ...], "note": null}

Errors (HTTP status → detail) 400 → bad_request (invalid input) 404 → not_found (upstream 404 or empty type result) 502 → upstream_error (bad/unexpected upstream response) 504 → upstream_timeout (network/timeout)

# 🔗 Upstream Mapping (for reference)
/jokes/random/ → GET /random_joke

/jokes/ten/ → GET /random_ten (or /jokes/ten)

/jokes/random/{n} → GET /jokes/random/{n}

/jokes/type/{joke_type}/random → GET /jokes/{type}/random (provider returns list[1])

/jokes/{id} → GET /jokes/{id}

# 🧪 Tests
pip install pytest respx httpx

pytest -q

All external calls are mocked with respx (no real internet).

Minimal suite covers happy paths + 400/404/502/504.

