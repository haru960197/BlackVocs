from fastapi import FastAPI
import uvicorn
import mongo_utils
import config
import service.app.schemas.user_schema as user_schema
import models

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return "成功！"


@app.post("/add_new_word", response_model=user_schema.AddNewWordResponse)
async def add_new_word(request: user_schema.AddNewWordRequest):
    """ 単語からitemを生成し，データベースに保存
    """
    word = request.word
    try:
        print("Received: ", word)
        new_item = mongo_utils.generate_and_insert_item(word)
        return user_schema.AddNewWordResponse(
            item=model_to_schema(new_item)
        )
    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}


@app.get("/items/all", response_model=user_schema.GetAllItemsResponse)
async def get_all_items():
    """ 全ての単語情報を取得
    """
    items = mongo_utils.get_all_items()
    return user_schema.GetAllItemsResponse(
        items=[model_to_schema(item) for item in items]
    )


def model_to_schema(item: models.Item) -> user_schema.Item:
    """ model.Itemからレスポンス用のschemas.Itemへ変更する
    """
    if not item.id:
        raise ValueError("Error: Failed to covert to schema from model. [item.id] is undefined.")
    
    return user_schema.Item(
        id=item.id,
        word=item.word,
        meaning=item.meaning,
        example_sentence=item.example_sentence,
        example_sentence_translation=item.example_sentence_translation
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.SERVICE_PORT, reload=True)
