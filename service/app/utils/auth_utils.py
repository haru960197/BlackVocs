from datetime import timedelta
from fastapi import Request, HTTPException, status
from jwt_auth import AuthJwtCsrt
import core.const as const

auth = AuthJwtCsrt()
ACCESS_TOKEN_EXPIRE_MINUTES = const.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(user_id: str) -> str:
    """Create signed JWT for given user_id."""
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return auth.encode_jwt(user_id, expires_delta=expire)

def decode_token(token: str) -> str:
    """Decode JWT and return subject (user_id)."""
    return auth.decode_jwt(token)

def strip_bearer_if_needed(token: str) -> str:
    """Allow both raw token and 'Bearer <token>' formats."""
    if token.startswith("Bearer "):
        return token[7:]
    return token

async def get_token_from_cookie(request: Request) -> str:
    """Extract JWT from cookie and normalize it."""
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return strip_bearer_if_needed(token)

async def get_user_id_from_cookie(request: Request) -> str:
    """Return user_id from cookie JWT."""
    token = await get_token_from_cookie(request)
    try:
        return decode_token(token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
