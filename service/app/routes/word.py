from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pymongo.database import Database
import utils.auth_utils as auth_utils
import schemas.common_schemas as common_schemas
from repositories.session import get_db
from services.word_service import WordService
import schemas.word_schemas as word_schemas
from utils.auth_utils import get_user_id_from_cookie
from utils.generative_AI_client import GenerativeAIClient
from models.word import Entry as word_entry

router = APIRouter(prefix="/word", tags=["word"])

@router.get(
    "/get_user_word_list", 
    operation_id="get_user_word_list", 
    response_model=word_schemas.GetUserWordListResponse, 
    responses=common_schemas.COMMON_ERROR_RESPONSES
)
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
    try: 
        entries = svc.get_word_entries_for_user(user_id)
        items = [word_schemas.Item(**entry.dict()) for entry in entries]
        return word_schemas.GetUserWordListResponse(items=items, userid=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error while getting items")

# @router.get(
#     "/suggest_words", 
#     response_model=word_schemas.SuggestWordsResponse, 
#     operation_id="suggest_words"
# )
# async def suggest_words(
#     q: str = Query(..., description="prefix / exact-first query"),
#     limit: int = Query(10, ge=1, le=50),
#     db: Database = Depends(get_db),
# ):
#     """Return suggestions (exact-first then prefix)."""
#     svc = WordService(db)
#     docs = svc.suggest_words(q=q, limit=limit)
#     items = [word_schemas.Item(**d) for d in docs]
#     return word_schemas.SuggestWordsResponse(items=items)

@router.post(
    "/generate_new_word_entry", 
    operation_id="generate_new_word_entry", 
    response_model=word_schemas.GenerateNewWordEntryResponse, 
    responses=common_schemas.COMMON_ERROR_RESPONSES, 
    description="generate new word entry with AI", 
)
async def generate_new_word_entry( 
    request: word_schemas.GenerateNewWordEntryRequest, 
):
    client = GenerativeAIClient()
    try:
        result: dict[str, str] | None = client.generate_entry(request.word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"item": result}

@router.post(
    "/register_word", 
    operation_id="register_word", 
    response_model=word_schemas.RegisterWordResponse, 
    status_code=status.HTTP_201_CREATED,
    responses=common_schemas.COMMON_ERROR_RESPONSES
)
async def register_word(
    payload: word_schemas.RegisterWordRequest,
    request: Request,
    db: Database = Depends(get_db),
):

    try:
        user_id = await get_user_id_from_cookie(request)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    svc = WordService(db)
    try:
        entry = word_entry(**payload.item.dict())  
        svc.register_word(entry, user_id)  
        item = word_schemas.Item.model_validate(entry, from_attributes=True)
        return word_schemas.RegisterWordResponse(item=item)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error during register_word")



    
