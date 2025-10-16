import respx
from httpx import Response, RequestError

BASE = "https://official-joke-api.appspot.com"

# ---------- health ----------
def test_health(client):
    r = client.get("/health/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

# ---------- /jokes/random ----------
@respx.mock
def test_random_ok(client):
    respx.get(f"{BASE}/random_joke").mock(
        return_value=Response(200, json={"id": 1, "type": "general", "setup": "s", "punchline": "p"})
    )
    r = client.get("/jokes/random/")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"id", "type", "setup", "punchline"}

@respx.mock
def test_random_upstream_timeout(client):
    respx.get(f"{BASE}/random_joke").mock(side_effect=RequestError("boom"))
    r = client.get("/jokes/random/")
    assert r.status_code == 504

# ---------- /jokes/ten ----------
@respx.mock
def test_ten_ok(client):
    respx.get(f"{BASE}/random_ten").mock(
        return_value=Response(
            200,
            json=[{"id": i, "type": "general", "setup": "s", "punchline": "p"} for i in range(10)],
        )
    )
    r = client.get("/jokes/ten/")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 10
    assert len(body["items"]) == 10

# ---------- /jokes/random/{n} ----------
@respx.mock
def test_random_n_ok(client):
    n = 3
    respx.get(f"{BASE}/jokes/random/{n}").mock(
        return_value=Response(
            200,
            json=[{"id": i, "type": "general", "setup": "s", "punchline": "p"} for i in range(n)],
        )
    )
    r = client.get(f"/jokes/random/{n}")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == n
    assert len(body["items"]) == n

def test_random_n_bad_request_low(client):
    r = client.get("/jokes/random/0")
    assert r.status_code == 400

def test_random_n_bad_request_high(client):
    r = client.get("/jokes/random/9999")
    assert r.status_code in (400, 422)  # зависит от твоей валидации

# ---------- /jokes/type/{type}/random ----------
@respx.mock
def test_type_random_ok(client):
    respx.get(f"{BASE}/jokes/programming/random").mock(
        return_value=Response(
            200,
            json=[{"id": 99, "type": "programming", "setup": "s", "punchline": "p"}],
        )
    )
    r = client.get("/jokes/type/programming/random")
    assert r.status_code == 200
    assert r.json()["type"] == "programming"

@respx.mock
def test_type_random_not_found(client):
    respx.get(f"{BASE}/jokes/foobar/random").mock(return_value=Response(200, json=[]))
    r = client.get("/jokes/type/foobar/random")
    assert r.status_code == 404

# ---------- /jokes/{id} ----------
@respx.mock
def test_by_id_ok(client):
    respx.get(f"{BASE}/jokes/1").mock(
        return_value=Response(200, json={"id": 1, "type": "general", "setup": "s", "punchline": "p"})
    )
    r = client.get("/jokes/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1

@respx.mock
def test_by_id_not_found(client):
    respx.get(f"{BASE}/jokes/999999").mock(return_value=Response(404))
    r = client.get("/jokes/999999")
    assert r.status_code == 404
