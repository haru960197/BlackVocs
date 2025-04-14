from fastapi import FastAPI
import uvicorn
import mongo_utils
import config
import schemas
import models

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return "成功！"


@app.post("/add_new_word", response_model=schemas.AddNewWordResponse)
async def add_new_word(request: schemas.AddNewWordRequest):
    """ 単語からitemを生成し，データベースに保存
    """
    word = request.word
    try:
        print("Received: ", word)
        new_item = mongo_utils.generate_and_insert_item(word)
        return schemas.AddNewWordResponse(
            item=model_to_schema(new_item)
        )
    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}


@app.get("/items/all", response_model=schemas.GetAllItemsResponse)
async def get_all_items():
    """ 全ての単語情報を取得
    """
    items = mongo_utils.get_all_items()
    return schemas.GetAllItemsResponse(
        items=[model_to_schema(item) for item in items]
    )


def model_to_schema(item: models.Item) -> schemas.Item:
    """ model.Itemからレスポンス用のschemas.Itemへ変更する
    """
    if not item.id:
        raise ValueError("Error: Failed to covert to schema from model. [item.id] is undefined.")
    
    return schemas.Item(
        id=item.id,
        word=item.word,
        meaning=item.meaning,
        example_sentence=item.example_sentence,
        example_sentence_translation=item.example_sentence_translation
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.SERVICE_PORT, reload=True)
