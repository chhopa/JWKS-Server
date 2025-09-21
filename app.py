"""Flask app exposing JWKS and JWT auth endpoints for assignment."""

from flask import Flask, jsonify, request
from key_store import KeyStore

app = Flask(__name__)

# Create and initialize one KeyStore instance
key_store = KeyStore()
key_store.init_keys()


@app.route("/")
def home():
    """Return basic info including student name and available endpoints."""
    return jsonify({
        "service": "JWKS demo",
        "student": "Tanchhopa Limbu Sanba",
        "endpoints": ["/jwks", "POST /auth", "POST /auth?expired=1"]
    })


@app.route("/jwks")
@app.route("/jwks.json")
@app.route("/.well-known/jwks.json")
def jwks():
    """Return the active JWKS (non-expired keys only)."""
    return jsonify(key_store.get_jwks())


@app.route("/auth", methods=["POST"])
def auth():
    """Return a signed JWT. If ?expired=1, return an expired token."""
    use_expired = "expired" in request.args
    token = key_store.issue_jwt(use_expired=use_expired)
    return jsonify({"token": token})


if __name__ == "__main__":
    app.run(port=8080)
