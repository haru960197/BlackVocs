import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import core.config as config
import core.const as const
from core.errors import TokenExpiredError, InvalidTokenError
from models.common import PyObjectId

JWT_KEY = config.JWT_KEY  
ACCESS_TOKEN_EXPIRE_MINUTES = const.ACCESS_TOKEN_EXPIRE_MINUTES

class AuthJwtCsrt:
    """
    Auth helper that handles password hashing and JWT encode/decode.
    """

    def __init__(
        self, 
        secret_key: str | None = None, 
        algorithm: str = "HS256",
    ):

        self.pwd_ctx = CryptContext(
            schemes=["bcrypt"], 
            deprecated="auto"
        )
        self.secret_key = (secret_key or JWT_KEY or "").strip()
        self.algorithm = algorithm

        if not self.secret_key:
            raise RuntimeError("JWT secret key is missing. Set JWT_KEY in your config/env.")

    # --- Access token ---
    def create_access_token(self, user_id: PyObjectId) -> str:
        """Create signed JWT for given user_id."""
        expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.encode_jwt(user_id, expires_delta=expire)

    # --- Password helpers ---
    def generate_hashed_pw(self, password: str) -> str:
        """Return bcrypt-hashed password."""
        return self.pwd_ctx.hash(password)

    def verify_pw(self, plain_pw: str, hashed_pw: str) -> bool:
        """Return True if plain password matches the hashed one."""
        return self.pwd_ctx.verify(plain_pw, hashed_pw)

    # --- JWT helpers ---
    def encode_jwt(
        self, 
        user_id: PyObjectId, 
        expires_delta: timedelta = timedelta(minutes=15)
    ) -> str:
        """
        Create a signed JWT with subject = user_id.
        - Uses UTC timestamps for iat/exp to avoid timezone issues.
        """
        now = datetime.now(timezone.utc)
        exp = now + expires_delta
        payload = {
            "sub": str(user_id), 
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_jwt(
        self, 
        token: str, 
        leeway_seconds: int = 0
    ) -> PyObjectId:
        """
        Decode JWT and return subject (user_id).
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
                raise InvalidTokenError("JWT 'sub' claim is missing")
            return sub

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("The JWT has expired")
        except (jwt.InvalidSignatureError, jwt.DecodeError, jwt.InvalidTokenError): 
            raise InvalidTokenError("JWT is invalid")
