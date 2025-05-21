from fastapi import APIRouter, Depends
from pymongo.database import Database
from db.session import get_db
import utils.word_utils as utils
import schemas.word_schemas as schemas

router = APIRouter()

@router.post("/word/add_new_word", response_model=schemas.AddNewWordResponse)
async def add_new_word(      
    request: schemas.AddNewWordRequest,
    db: Database = Depends(get_db)
):
    """単語から item を生成し、データベースに保存"""
    word = request.word
    try:
        new_item: schemas.Item = utils.generate_and_insert_item(word, db)
        return schemas.AddNewWordResponse(
            item=utils.model_to_schema(new_item)
        )
    except Exception as e:
        print("Error occurred:", e)
        raise e  

# @router.post("/word/add_new_word_with_userid", response_model=schemas.AddNewWordWithUseridResponse) 
# async def add_new_word_with_userid(
    
# )

