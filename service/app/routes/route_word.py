from fastapi import APIRouter
from schemas import word_schemas, user_schemas
import mongo_utils
import models

router = APIRouter()

@router.post("/add_new_word", response_model=word_schemas.AddNewWordResponse)
async def add_new_word(request: word_schemas.AddNewWordRequest):
    """単語からitemを生成し，データベースに保存"""
    word = request.word
    try:
        print("Received: ", word)
        new_item = mongo_utils.generate_and_insert_item(word)
        return word_schemas.AddNewWordResponse(
            item=model_to_schema(new_item)
        )
    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}

@router.get("/items/all", response_model=word_schemas.GetAllItemsResponse)
async def get_all_items():
    """全ての単語情報を取得"""
    items = mongo_utils.get_all_items()
    return word_schemas.GetAllItemsResponse(
        items=[model_to_schema(item) for item in items]
    )

def model_to_schema(item: models.Item) -> word_schemas.Item:
    """model.Itemからレスポンス用のschemas.Itemへ変換"""
    if not item.id:
        raise ValueError("Error: Failed to covert to schema from model. [item.id] is undefined.")

    return word_schemas.Item(
        id=item.id,
        word=item.word,
        meaning=item.meaning,
        example_sentence=item.example_sentence,
        example_sentence_translation=item.example_sentence_translation
    )
