"""RSA key management and JWT issuance for JWKS server assignment."""

import time
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt

MINUTE = 60


class KeyStore:
    """Manages RSA keys (active + expired) and issues JWTs."""

    def __init__(self) -> None:
        """Initialize an empty key store."""
        self.keys = []

    def _make_rsa_key(self, ttl_seconds: int, start_offset: int = 0) -> dict:
        """Generate an RSA keypair with a kid and not_after expiry time."""
        # Create private + public keypair
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        
        # Assign a unique key ID (kid) and set validity window
        kid = str(uuid.uuid4())
        now = int(time.time()) + start_offset
        not_after = now + ttl_seconds

        # Serialize public key for JWKS publishing
        pub_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return {
            "kid": kid,
            "private_key": private_key,
            "public_pem": pub_pem.decode(),
            "not_after": not_after,
        }

    def init_keys(self) -> None:
        """Initialize with one active key and one already expired key."""
        # Expired key: expired 10 minutes ago
        expired_key = self._make_rsa_key(5 * MINUTE, start_offset=-(15 * MINUTE))
        # Active key: valid for 1 hour
        active_key = self._make_rsa_key(60 * MINUTE)
        self.keys = [expired_key, active_key]

    def rotate_key(self, ttl_seconds: int = 60 * MINUTE) -> dict:
        """Add a new active key (for future rotation extensions)."""
        new_key = self._make_rsa_key(ttl_seconds)
        self.keys.append(new_key)
        return new_key

    def get_jwks(self) -> dict:
        """Return JWKS with all non-expired keys."""
        now = int(time.time())
        keys = []
        for key in self.keys:
            if key["not_after"] > now:
                n = key["private_key"].public_key().public_numbers().n
                e = key["private_key"].public_key().public_numbers().e
                keys.append({
                    "kty": "RSA",
                    "use": "sig",
                    "alg": "RS256",
                    "kid": key["kid"],
                    "n": jwt.utils.base64url_encode(
                        n.to_bytes((n.bit_length() + 7) // 8, "big")
                    ).decode(),
                    "e": jwt.utils.base64url_encode(
                        e.to_bytes((e.bit_length() + 7) // 8, "big")
                    ).decode()
                })
        return {"keys": keys}

    def issue_jwt(self, use_expired: bool = False) -> str:
        """Issue a JWT with either the active key or a forced expired key."""
        now = int(time.time())
        active_keys = [k for k in self.keys if k["not_after"] > now]
        expired_keys = [k for k in self.keys if k["not_after"] <= now]

        # Pick key depending on expired flag
        if use_expired and expired_keys:
            slot = expired_keys[-1]    # most recent expired
            exp = now - 30             # expires in 5 minutes
        else:
            slot = active_keys[-1]    # most recent active
            exp = now + 5 * MINUTE    # expires in 5 minutes

        # Sign a JWT with chosen key
        token = jwt.encode(
            {
                "sub": "mock-user-123",
                "iat": now,
                "exp": exp,
                "iss": "jwks-demo",
                "aud": "jwks-demo-client",
            },
            slot["private_key"],
            algorithm="RS256",
            headers={"kid": slot["kid"]}
        )
        return token
