from fastapi import status
from typing import Dict, Any
from pydantic import BaseModel, Field

class SuccessMsg(BaseModel):
    message: str

class GeneralErrorResponse(BaseModel):
    detail: str = Field(..., description="エラーメッセージ（文字列）")

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
    status.HTTP_404_NOT_FOUND: {
        "description": "リソースが存在しない",
        "model": GeneralErrorResponse,
    },
    status.HTTP_409_CONFLICT: {
        "description": "コンフリクト発生",
        "model": GeneralErrorResponse,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "バリデーションエラー",
        "model": GeneralErrorResponse,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "サーバー内部エラー",
        "model": GeneralErrorResponse,
    },
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "description": "サービス利用不可",
        "model": GeneralErrorResponse,
    },
}
