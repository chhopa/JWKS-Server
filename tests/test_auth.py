import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import jwt
import app


@pytest.fixture
def client():
    """Provide a Flask test client."""
    app.app.config["TESTING"] = True
    with app.app.test_client() as c:
        yield c


def test_auth_returns_valid_jwt(client):
    """Ensure /auth returns a valid, unexpired JWT with a kid in the header."""
    res = client.post("/auth")
    assert res.status_code == 200
    token = res.get_json()["token"]
    header = jwt.get_unverified_header(token)
    assert "kid" in header
    payload = jwt.decode(token, options={"verify_signature": False})
    assert payload["sub"] == "mock-user-123"
    assert payload["exp"] > payload["iat"]


def test_auth_expired_token(client):
    """Ensure /auth?expired=1 returns a token that is already expired."""
    res = client.post("/auth?expired=1")
    assert res.status_code == 200
    token = res.get_json()["token"]
    payload = jwt.decode(token, options={"verify_signature": False})
    assert payload["exp"] < payload["iat"]
