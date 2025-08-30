from fastapi import APIRouter, Depends, status
from pymongo.database import Database
import schemas.common_schemas as common_schemas
from repositories.session import get_db
from services.word_service import WordService
import schemas.word_schemas as word_schemas
from utils.auth_utils import get_user_id_from_cookie
from models.word import Entry

router = APIRouter(prefix="/word", tags=["word"], responses=common_schemas.COMMON_ERROR_RESPONSES)

@router.get(
    "/get_user_word_list", 
    operation_id="get_user_word_list", 
    response_model=word_schemas.GetUserWordListResponse, 
)
async def get_user_word_list(
    user_id: str = Depends(get_user_id_from_cookie),
    db: Database = Depends(get_db)
):
    """Return the current user's saved word list."""
    svc = WordService(db)
    model_items = svc.get_word_items_for_user(user_id)
    schema_items = [model_item.to_schema_item() for model_item in model_items]
    return word_schemas.GetUserWordListResponse(items=schema_items, userid=user_id)

@router.post(
    "/suggest_words", 
    response_model=word_schemas.SuggestWordsResponse, 
    operation_id="suggest_words",
)
async def suggest_words(
    request: word_schemas.SuggestWordsRequest,
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    CANDIDATE_CAP = 100

    items = svc.suggest_items(
        input_word=request.input_word, 
        limit=request.limit, 
        cap=CANDIDATE_CAP, 
    )
    return word_schemas.SuggestWordsResponse(items=[it.to_schema_item() for it in items])

@router.post(
    "/generate_new_word_entry", 
    operation_id="generate_new_word_entry", 
    response_model=word_schemas.GenerateNewWordEntryResponse, 
    description="generate new word entry with AI", 
)
async def generate_new_word_entry( 
    payload: word_schemas.GenerateNewWordEntryRequest, 
    user_id: str = Depends(get_user_id_from_cookie),
):
    from utils.generative_AI_client import GenerativeAIClient
    client = GenerativeAIClient()
    generated_entry: Entry = client.generate_entry(payload.word)
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
    user_id: str = Depends(get_user_id_from_cookie),
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    entry = Entry(**payload.item.dict())  
    registered_id = svc.register_word(entry, user_id)  
    return word_schemas.RegisterWordResponse(user_word_id=registered_id)
