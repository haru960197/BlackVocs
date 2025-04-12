# start application
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 
import mongo_utils
import config
from db.session import client, get_db

app = FastAPI()

@app.on_event("shutdown")
def shutdown_event():
    client.close()

@app.get("/", status_code=200)
def root():
    return "成功！"

@app.post("/box", status_code=200)
def post_item_in_box(item: str):
    # dbというデータベースを取得
    db = get_db()
    # データベースにデータを追加
    result = db["box"].insert_one({"item": item})
    return {"id": str(result.inserted_id)}


@app.get("/box", status_code=200)
def get_items_in_box():
    # dbというデータベースを取得
    db = get_db()
    # データベースからデータを取得
    items = db["box"].find()
    # データを整形
    results = [{"id": str(item["_id"]), "item": item["item"]} for item in items]
    return results

# リクエストボディの型定義
class Item(BaseModel):
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str 

# POSTで受け取ったItemをMongoDBに保存
@app.post("/dictionary/")
async def insert_item(item: Item):
    print("Received: ", item)
    inserted_id = mongo_utils.insert_item(item)  # Mongoに保存
    return {"message": f"Item '{item.name}' was saved.", "id": inserted_id}

@app.post("/new_word/")
async def insert_new_word(word: str):
    """
    単語からitemを生成し，データベースに保存
    """
    try:
        print("Received: ", word)
        inserted_id = mongo_utils.generate_and_insert_item(word)
        return {"message": f"Item '{word}' was saved."}
    except Exception as e:
        print("Error occurred:", e)
        return {"error": str(e)}
        


@app.get("/items/all")
async def read_all_items():
    items = mongo_utils.get_all_items()
    return {"items": items}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.SERVICE_PORT, reload=True)
