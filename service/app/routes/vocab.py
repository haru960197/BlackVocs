from fastapi import APIRouter, Depends
from pymongo.database import Database
from db.session import get_db
import utils.vocab_utils as utils
from schemas.vocab_schemas import (
    Item,
    AddNewWordResponse,
    AddNewWordRequest,
)

router = APIRouter()

@router.post("/vocab/add_new_word", response_model=AddNewWordResponse)
async def add_new_word(      
    request: AddNewWordRequest,
    db: Database = Depends(get_db)
):
    """単語から item を生成し、データベースに保存"""
    word = request.word
    try:
        new_item: Item = utils.generate_and_insert_item(word, db)
        return AddNewWordResponse(
            item=utils.model_to_schema(new_item)
        )
    except Exception as e:
        print("Error occurred:", e)
        raise e  


