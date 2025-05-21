from datetime import timedelta 
from fastapi import Request, HTTPException, status, Depends
from db.session import get_db
from schemas.user_schemas import  (
    User,
    UserInDB,
    TokenData,
) 
from pymongo.database import Database
import core.config as config
import core.const as const
from jwt_auth import AuthJwtCsrt

USER_COLLECTION_NAME = config.USER_COLLECTION_NAME
ACCESS_TOKEN_EXPIRE_MINUTES = const.ACCESS_TOKEN_EXPIRE_MINUTES

auth = AuthJwtCsrt()

def get_user(db: Database, username: str) -> UserInDB | None:
    user_data = db[USER_COLLECTION_NAME].find_one({"username": username})
    if user_data:
        return UserInDB.model_validate(user_data)
    return None

async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    return token

async def get_current_user(
    token: str = Depends(get_token_from_cookie),
    db: Database = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = auth.decode_jwt(token)
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except HTTPException:
        raise credentials_exception

    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_access_token(user_id: str) -> str:
    """user_idを入力とし、jwtトークンを生成"""
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.encode_jwt(user_id, expires_delta=expire)
    return token

async def get_user_id_from_cookie(request: Request) -> str:
    """
    Cookie に含まれる JWT から user_id を取得して返す。

    Raises:
        HTTPException: Cookie が無い、または JWT が無効な場合
    """
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found in cookie"
        )

    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "", 1)

    return auth.decode_jwt(token)
