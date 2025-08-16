from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from typing import Tuple, List
from pymongo.database import Database
import utils.auth_utils as auth_utils
import schemas.common_schemas as common_schemas
from repositories.session import get_db
from services.word_service import WordService
import schemas.word_schemas as word_schemas
from utils.auth_utils import get_user_id_from_cookie
from utils.generative_AI_client import GenerativeAIClient
from models.word import Entry, Item

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
        model_items = svc.get_word_items_for_user(user_id)
        schema_items = [model_item.to_schema_item() for model_item in model_items]
        return word_schemas.GetUserWordListResponse(items=schema_items, userid=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error while getting items")

@router.post(
    "/suggest_words", 
    response_model=word_schemas.SuggestWordsResponse, 
    operation_id="suggest_words",
    responses=common_schemas.COMMON_ERROR_RESPONSES
)
async def suggest_words(
    request: word_schemas.SuggestWordsRequest,
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    input_word = request.input_word
    limit = request.limit
    if not input_word:
        raise HTTPException(status_code=400, detail="input_word is required.")
    CANDIDATE_CAP = 100

    # 正規表現を用いてDBから候補となる単語のリストを取得
    candidate_items = svc.make_candidates_from_word(input_word, CANDIDATE_CAP)

    if not candidate_items:
        return word_schemas.SuggestWordsResponse(items=[])

    # LCS(最長共通部分裂)の長さで候補の単語をスコアリングする
    score_items: List[Tuple[float, Item]] = []  # (score, Item)
    input_word = input_word.lower()
    for item in candidate_items:
        word = item.entry.word
        if not word:
            continue
        score = svc.lcs_score(input_word, word.lower())
        score_items.append((score, item))

    # 独自の優先度(score > registered_count > len(word) > wordの辞書順)で降順にソート
    score_items.sort(key=lambda t: (-t[0], -t[1].registered_count, len(t[1].entry.word), t[1].entry.word))

    items = [word_info[1].to_schema_item() for word_info in score_items[:limit]]
    return word_schemas.SuggestWordsResponse(items=items)

@router.post(
    "/generate_new_word_entry", 
    operation_id="generate_new_word_entry", 
    response_model=word_schemas.GenerateNewWordEntryResponse, 
    responses=common_schemas.COMMON_ERROR_RESPONSES, 
    description="generate new word entry with AI", 
)
async def generate_new_word_entry( 
    request: Request,
    payload: word_schemas.GenerateNewWordEntryRequest, 
):
    try: 
        user_id = await get_user_id_from_cookie(request)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    client = GenerativeAIClient()
    try:
        generated_entry: Entry = client.generate_entry(payload.word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return word_schemas.GenerateNewWordEntryResponse(item=generated_entry.to_schema_item())

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
        entry = Entry(**payload.item.dict())  
        registered_id = svc.register_word(entry, user_id)  
        return word_schemas.RegisterWordResponse(user_word_id=registered_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error during register_word")



    
