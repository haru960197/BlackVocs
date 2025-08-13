from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pymongo.database import Database
import utils.word as word_utils
import utils.user as auth_utils
import utils.user_word as user_word_utils
import schemas.common_schemas as common_schemas
import schemas.word as schemas
import models.word as word_models
from repositories.session import get_db
from services.word_service import WordService
from schemas.word import (
    AddNewWordRequest,
    AddNewWordResponse,
    GetUserWordListResponse,
    SuggestWordsResponse,
    Item as ItemSchema,
)
from utils.auth_utils import get_user_id_from_cookie  # cookie から user_id を取る既存関数

router = APIRouter(prefix="/word", tags=["word"])

@router.post("/add_new_word", operation_id="add_new_word", response_model=AddNewWordResponse, responses=common_schemas.COMMON_ERROR_RESPONSES)
async def add_new_word(
    payload: AddNewWordRequest,
    request: Request,
    db: Database = Depends(get_db),
):
    """Generate a word via DeepSeek (if needed), insert it, and link to current user."""

    try:
        user_id = await get_user_id_from_cookie(request)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    svc = WordService(db)
    try:
        word_doc, link_id = svc.add_new_word(payload.word, user_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to add new word: {e}")

    # NOTE: response_model is camelCase via alias generator in your schema
    return AddNewWordResponse(
        item=ItemSchema(**word_doc),
        user_word_id=link_id or "",  # empty if already linked (or you can return existing id)
    )

@router.get("/get_user_word_list", operation_id="get_user_word_list", response_model=GetUserWordListResponse, responses=common_schemas.COMMON_ERROR_RESPONSES)
async def get_user_word_list(
    request: Request,
    db: Database = Depends(get_db)
):
    """Return the current user's saved word list."""
    try:
        user_id = await auth_utils.get_user_id_from_cookie(request)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    svc = WordService(db)
    docs = svc.get_user_word_list(user_id)
    items = [ItemSchema(**d) for d in docs]
    return GetUserWordListResponse(wordlist=items, userid=user_id)

@router.get("/suggest_words", response_model=SuggestWordsResponse, operation_id="suggest_words")
async def suggest_words(
    q: str = Query(..., description="prefix / exact-first query"),
    limit: int = Query(10, ge=1, le=50),
    db: Database = Depends(get_db),
):
    """Return suggestions (exact-first then prefix)."""
    svc = WordService(db)
    docs = svc.suggest_words(q=q, limit=limit)
    items = [ItemSchema(**d) for d in docs]
    return SuggestWordsResponse(items=items)
