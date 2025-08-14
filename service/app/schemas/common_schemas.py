# common_schemas.py
from fastapi import status
from typing import Dict, Any
from pydantic import BaseModel, Field

class SuccessMsg(BaseModel):
    message: str

class GeneralErrorResponse(BaseModel):
    detail: str = Field(..., description="エラーメッセージ（文字列）")

# 共通の responses 定義（400／401／403／500 はすべて同じモデルを使う例）
COMMON_ERROR_RESPONSES: Dict[int | str, Dict[str, Any]] = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "リクエスト不正",
        "model": GeneralErrorResponse,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "認証失敗",
        "model": GeneralErrorResponse,
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "権限なし",
        "model": GeneralErrorResponse,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "サーバー内部エラー",
        "model": GeneralErrorResponse,
    },
}
