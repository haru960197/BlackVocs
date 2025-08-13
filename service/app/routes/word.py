from typing import List
from fastapi import APIRouter, Depends, Query, Request, HTTPException 
from pymongo.database import Database
from db.session import get_db
import utils.word as word_utils
import utils.user as auth_utils
import utils.user_word as user_word_utils
import schemas.word as schemas
import models.word as word_models

router = APIRouter()


@router.post("/word/add_new_word", response_model=schemas.AddNewWordResponse)
async def add_new_word(      
    request: Request,
    word_request: schemas.AddNewWordRequest,
    db: Database = Depends(get_db)
):
    """
    input: an English word

    1. 単語入力からアイテムを生成
    2. ItemをDBに登録
    3. cookieからuser_id取得
    4. user_wordテーブルにuser_id, word_idを保存

    return: itemのid, user_wordテーブルid
    """
    word = word_request.word

    # 1. アイテム生成
    try:
        new_item: word_models.Item = word_utils.word2item_with_API(word)
    except Exception as e:
        print("Error occurred in item generation:", e)
        raise e  
    
    # 2. ItemをDBに登録
    try: 
        word_id: str = word_utils.insert_word_item(new_item, db)
    except Exception as e:
        print("Error occurred in item insertion:", e)
        raise e  

    # 3. cookieからuser_id取得
    try: 
        user_id: str = await auth_utils.get_user_id_from_cookie(request)
    except Exception as e:
        print("Error occurred in user ID retrieval:", e)
        raise e   

    # 4. user_wordテーブルに保存
    try: 
        user_word_id = user_word_utils.insert_user_word(user_id, word_id, db)
    except Exception as e: 
        print("Error occured in user_word_item insertion:", e)
        raise HTTPException(status_code=500, detail="Failed to insert user-word item") 

    return schemas.AddNewWordResponse(
        item=word_utils.model_to_schema(new_item),
        user_word_id=user_word_id
    )

@router.get("/word/get_user_word_list", response_model=schemas.GetUserWordListResponse)
async def get_user_word_list(
    request: Request,
    db: Database = Depends(get_db)
):
    """
    Get the list of words saved by the current user.
    """
    # 1. get user_id 
    try:
        user_id: str = await auth_utils.get_user_id_from_cookie(request)
    except Exception as e:
        print("Error occurred in user ID retrieval:", e)
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2. get word_id list from user_word_db
    try:
        word_ids: list[str] = user_word_utils.get_user_word_ids(user_id, db)
    except Exception as e:
        print("Error retrieving user word list:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve word list")

    # 3. word item list from word_db
    try:
        items: list[word_models.Item] = word_utils.get_items_by_ids(word_ids, db)
    except Exception as e:
        print("Error retrieving items from word IDs:", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve word details")

    return schemas.GetUserWordListResponse(
        wordlist=[word_utils.model_to_schema(item) for item in items],
        userid=user_id
    )

# for test 
@router.get("/word/suggest", response_model=schemas.SuggestWordsResponse) 
async def suggest_words( 
    q: str = Query(..., min_length=1, max_length=64, description="prefix or exact text"), 
    limit: int = Query(10, ge=10, le=50), 
    case_insensitive: bool = Query(True, description="ignore whether upper or lowercase"),
    db: Database = Depends(get_db), 
): 
    """
    入力文字列 q に対して、word フィールドのスペルが一致（完全一致を優先・前方一致で補完）
    するアイテムを最大 limit 件返す。
    """

    try:
        items: List[word_models.Item] = word_utils.find_items_by_spelling(
            q=q, db=db, limit=limit, case_insensitive=case_insensitive
        )
    except Exception as e:
        print("Error occurred in suggest_words:", e)
        raise HTTPException(status_code=500, detail="Failed to search suggestions")

    return schemas.SuggestWordsResponse(
        items=[word_utils.model_to_schema(it) for it in items]
    )
