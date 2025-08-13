import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import core.config as config

JWT_KEY = config.JWT_KEY  # MUST be a non-empty string

class AuthJwtCsrt:
    """
    Auth helper that handles password hashing and JWT encode/decode.
    """

    def __init__(self, secret_key: str | None = None, algorithm: str = "HS256"):
        # Use instance attributes (easier to test/override)
        self.pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = (secret_key or JWT_KEY or "").strip()
        self.algorithm = algorithm

        # Fail fast if key is not configured
        if not self.secret_key:
            raise RuntimeError("JWT secret key is missing. Set JWT_KEY in your config/env.")

    # -------- Password helpers --------
    def generate_hashed_pw(self, password: str) -> str:
        """Return bcrypt-hashed password."""
        return self.pwd_ctx.hash(password)

    def verify_pw(self, plain_pw: str, hashed_pw: str) -> bool:
        """Return True if plain password matches the hashed one."""
        return self.pwd_ctx.verify(plain_pw, hashed_pw)

    # -------- JWT helpers --------
    def encode_jwt(self, user_id: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        """
        Create a signed JWT with subject = user_id.
        - Uses UTC timestamps for iat/exp to avoid timezone issues.
        """
        now = datetime.now(timezone.utc)
        exp = now + expires_delta
        payload = {
            "sub": user_id,
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_jwt(self, token: str, leeway_seconds: int = 0) -> str:
        """
        Decode JWT and return subject (user_id).
        - Accepts optional leeway to tolerate small clock skews.
        - Raises HTTP 401 on any invalid token.
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"require": ["sub", "exp", "iat"]},
                leeway=leeway_seconds,
            )
            sub = payload.get("sub")
            if not sub:
                raise HTTPException(status_code=401, detail="JWT 'sub' claim is missing")
            return sub

        except jwt.ExpiredSignatureError:
            # Token is expired
            raise HTTPException(status_code=401, detail="The JWT has expired")
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="JWT signature is invalid")
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="JWT is malformed or could not be decoded")
        except jwt.InvalidTokenError:
            # Generic invalid token
            raise HTTPException(status_code=401, detail="JWT is not valid")
