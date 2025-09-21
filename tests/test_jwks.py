import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import app


@pytest.fixture
def client():
    """Provide a Flask test client."""
    app.app.config["TESTING"] = True
    with app.app.test_client() as c:
        yield c


def test_jwks_excludes_expired(client):
    """Ensure /jwks excludes expired keys from the JWKS set."""
    res = client.get("/jwks")
    assert res.status_code == 200
    data = res.get_json()
    assert "keys" in data
    kids = [k["kid"] for k in data["keys"]]

    # expired key (first in the store) should not be included
    assert app.key_store.keys[0]["kid"] not in kids
