from fastapi import APIRouter, Depends, Request, HTTPException
from pymongo.database import Database
from db.session import get_db
import utils.word as word_utils
import utils.auth as auth_utils
import schemas.word as schemas
import models.word as word_models

router = APIRouter()

@router.post("/word/add_new_word", response_model=schemas.AddNewWordResponse)
async def add_new_word(      
    request: schemas.AddNewWordRequest,
    db: Database = Depends(get_db)
):
    """
    1. 単語入力からアイテムを生成
    input: str

    2. ItemをDBに登録
    input: Item
    output: 登録されたItemのID

    3. cookieからuser_id取得

    4. user_wordテーブルにuser_id, word_idを保存

    return user_word_id
    """
    word = request.word

    # 1. アイテム生成
    try:
        new_item: word_models.Item = word.word2item_with_API(word)
        return schemas.AddNewWordResponse(
            item=word.model_to_schema(new_item)
        )
    except Exception as e:
        print("Error occurred:", e)
        raise e  
