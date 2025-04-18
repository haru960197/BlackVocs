from fastapi import APIRouter
from fastapi import Response, Request
from fastapi.encoders import jsonable_encoder
from service.app.schemas.word_schemas import UserBody, SuccessMsg, UserInfo
from database import (
    db_signup,
    db_login,
)
from auth_utils import AuthJwtCsrt

router = APIRouter()
auth = AuthJwtCsrt()

# 新規登録
@router.post("/api/register", response_model=UserInfo)
async def signup(user: UserBody):
    user = jsonable_encoder(user) # dict型に変換
    new_user = await db_signup(user)
    return new_user

# ログイン
@router.post("/api/login", response_model=SuccessMsg)
async def login(response: Response, user:UserBody):
    user = jsonable_encoder(user) # dict型に変換
    token = await db_login(user)
    response.set_cookie( # クッキーに設定
        key="access_token", value=f"Bearer {token}", httponly=True, samesite="none", secure=True
    )
    return {"message": "Successfully logged-in"}
