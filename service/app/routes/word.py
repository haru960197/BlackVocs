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

@router.get(
    "/suggest_words", 
    response_model=word_schemas.SuggestWordsResponse, 
    operation_id="suggest_words"
    responses=common_schemas.common_schemas.COMMON_ERROR_RESPONSES
)
async def suggest_words(
    limit: int = Query(10, ge=1, le=50),
    db: Database = Depends(get_db),
):
    svc = WordService(db)
    query = q.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query 'q' must be non-empty.")

    subseq = svc.make_subsequence_regex(query)
    regex = {"$regex": subseq, "$options": "i"}  # case-insensitive

    # Tune this cap based on your data size & latency budget.
    CANDIDATE_CAP = 300

    # Project minimal fields to reduce payload.
    cursor = db["items"].find(
        {"entry.word": regex},
        {"entry.word": 1, "registered_count": 1}
    ).limit(CANDIDATE_CAP)

    candidates = list(cursor)

    if not candidates:
        return word_schemas.SuggestWordsResponse(suggestions=[])

    # --- 2) Score by true LCS ---
    scored: List[Tuple[float, int, str]] = []  # (score, registered_count, word)
    q_lower = query.lower()
    for doc in candidates:
        word = str(doc.get("entry", {}).get("word", ""))
        if not word:
            continue
        score = lcs_score(q_lower, word.lower())
        reg_cnt = int(doc.get("registered_count", 0))
        scored.append((score, reg_cnt, word))

    # --- 3) Sort: LCS desc, registered_count desc, len asc, word asc ---
    scored.sort(key=lambda t: (-t[0], -t[1], len(t[2]), t[2]))

    # --- 4) Build response (adjust to your schema) ---
    # 例: SuggestWordsResponse = { suggestions: List[SuggestedItem] }
    # SuggestedItem は { word: str, score: float, registered_count: int } を想定
    suggestions = [
        word_schemas.SuggestedItem(word=w, score=float(s), registered_count=rc)
        for s, rc, w in scored[:limit]
    ]
    return word_schemas.SuggestWordsResponse(suggestions=suggestions)

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



    
