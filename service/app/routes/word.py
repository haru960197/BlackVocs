from fastapi import APIRouter, Depends
from pymongo.database import Database
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from core.oid import PyObjectId
import schemas.common_schemas as common_schemas
from repositories.session import get_db
from services.word_service import WordService
from services.auth_service import AuthService 
from services.generativeAI_service import GenerativeAIService
import schemas.word_schemas as word_schemas

router = APIRouter(prefix="/word", tags=["word"], responses=common_schemas.COMMON_ERROR_RESPONSES)

@router.get(
    "/get_user_word_list", 
    operation_id="get_user_word_list", 
    response_model=word_schemas.GetUserWordListResponse, 
)
async def get_user_word_list(
    user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie),
    db: Database = Depends(get_db)
):
    svc = WordService(db)
    return svc.get_user_word_list_by_user_id(user_id)

@router.post(
    "/suggest_words", 
    operation_id="suggest_words",
    response_description="make suggestion for user's input", 
    response_model=word_schemas.SuggestWordsResponse, 
)
async def suggest_words(
    payload: word_schemas.SuggestWordsRequest,
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    return svc.generate_word_suggestion(payload)

@router.post(
    "/generate_new_word_entry", 
    operation_id="generate_new_word_entry", 
    response_description="generate new word entry with AI", 
    response_model=word_schemas.GenerateNewWordEntryResponse, 
)
async def generate_new_word_entry( 
    payload: word_schemas.GenerateNewWordEntryRequest, 
    _user_id: str = Depends(AuthService.get_user_id_from_cookie), 
):
    svc = GenerativeAIService()
    return svc.generate_word_entry(payload)

@router.post(
    "/register_word", 
    operation_id="register_word", 
    response_description="register a new item for the current user", 
    status_code=HTTP_200_OK, 
)
async def register_word(
    payload: word_schemas.RegisterWordRequest,
    user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie),
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    svc.register_word(payload, user_id)
    return 

@router.post(
    "/delete_word", 
    operation_id="delete_word", 
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_word(
    payload: word_schemas.DeleteWordRequest, 
    _user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie), 
    db: Database = Depends(get_db), 
): 
    svc = WordService(db)
    svc.delete_word(payload)
    return
