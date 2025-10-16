from fastapi import APIRouter, Depends, Response, status
from pymongo.database import Database
from core.oid import PyObjectId
from models.word import WordBaseModel, WordEntryModel, ExampleBaseModel
from models.common import AIGenerateModel
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
    response_description="get word item list that the current user has registered", 
    response_model=word_schemas.GetUserWordListResponse, 
)
async def get_user_word_list(
    user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie),
    db: Database = Depends(get_db)
):
    """Return the current user's saved word list."""
    svc = WordService(db)
    word_models = svc.get_user_word_list_by_user_id(user_id)
    return word_schemas.GetUserWordListResponse(
        word_list=[item.to_schema() for item in word_models]
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

    models = svc.collect_suggest_models(
        input_word=request.input_word, 
        limit=request.max_num, 
        cap=CANDIDATE_CAP, 
    )
    return word_schemas.SuggestWordsResponse(word_list=[it.to_schema() for it in models])

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

    word_base = WordBaseModel(
        word=payload.word, 
        meaning=payload.meaning,
    )
    example_base = ExampleBaseModel(
        example_sentence=payload.example_sentence, 
        example_sentence_translation=payload.example_sentence_translation,
    )
    entry_model = AIGenerateModel(
        word_base=word_base, 
        example_base=example_base, 
    )

    generated_entry = svc.generate_entry(entry_model)
    return generated_entry.to_schema()

@router.post(
    "/register_word", 
    operation_id="register_word", 
    response_description="register a new item for the current user", 
    response_model=word_schemas.RegisterWordResponse, 
)
async def register_word(
    payload: word_schemas.RegisterWordRequest,
    user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie),
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    word_base_model = WordBaseModel(
        word=payload.word, 
        meaning=payload.meaning, 
    )
    example_base_model = ExampleBaseModel(
        example_sentence=payload.example_sentence, 
        example_sentence_translation=payload.example_sentence_translation
    )
    word_entry = WordEntryModel(
        word_base=word_base_model, 
        example_base=example_base_model, 
    )
    registered_id = svc.register_word(word_entry, user_id)  
    return word_schemas.RegisterWordResponse(user_word_id=str(registered_id))

@router.post(
    "/delete_word", 
    operation_id="delete_word", 
    status_code=204,
)
async def delete_word(
    payload: word_schemas.DeleteWordRequest, 
    user_id: PyObjectId = Depends(AuthService.get_user_id_from_cookie), 
    db: Database = Depends(get_db), 
): 
    svc = WordService(db)
    deleted_id = svc.delete_word(PyObjectId(payload.word_id), user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
