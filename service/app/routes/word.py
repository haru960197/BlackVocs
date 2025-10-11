from fastapi import APIRouter, Depends, Response, status
from pymongo.database import Database
import schemas.common_schemas as common_schemas
from repositories.session import get_db
from services.word_service import WordService
from services.auth_service import AuthService 
from services.generativeAI_service import GenerativeAIService
import schemas.word_schemas as word_schemas
from models.word import Entry

router = APIRouter(prefix="/word", tags=["word"], responses=common_schemas.COMMON_ERROR_RESPONSES)

@router.get(
    "/get_user_word_list", 
    operation_id="get_user_word_list", 
    response_description="get word item list that the current user has registered", 
    response_model=word_schemas.GetUserWordListResponse, 
)
async def get_user_word_list(
    user_id: str = Depends(AuthService.get_user_id_from_cookie),
    db: Database = Depends(get_db)
):
    """Return the current user's saved word list."""
    svc = WordService(db)
    items = svc.get_word_items_by_user_id(user_id)
    return word_schemas.GetUserWordListResponse(
        items=[item.to_schema_item() for item in items]
    )

@router.post(
    "/suggest_words", 
    operation_id="suggest_words",
    response_description="suggest words according to the input", 
    response_model=word_schemas.SuggestWordsResponse, 
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
    response_description="generate new word entry with AI", 
    response_model=word_schemas.GenerateNewWordEntryResponse, 
)
async def generate_new_word_entry( 
    payload: word_schemas.GenerateNewWordEntryRequest, 
    user_id: str = Depends(AuthService.get_user_id_from_cookie), # only for auth check
):
    svc = GenerativeAIService()
    generated_entry = svc.generate_entry(payload.word)
    return word_schemas.GenerateNewWordEntryResponse(item=generated_entry.to_schema_item())

@router.post(
    "/register_word", 
    operation_id="register_word", 
    response_description="register a new item for the current user", 
    response_model=word_schemas.RegisterWordResponse, 
)
async def register_word(
    payload: word_schemas.RegisterWordRequest,
    user_id: str = Depends(AuthService.get_user_id_from_cookie),
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    entry = Entry(**payload.dict())  
    registered_id = svc.register_word(entry, user_id)  
    return word_schemas.RegisterWordResponse(user_word_id=registered_id)

@router.post(
    "/delete_word", 
    operation_id="delete_word", 
    status_code=204,
)
async def delete_word(
    payload: word_schemas.DeleteWordRequest, 
    user_id: str = Depends(AuthService.get_user_id_from_cookie), 
    db: Database = Depends(get_db), 
): 
    svc = WordService(db)
    deleted_id = svc.delete_user_item(payload.word_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
