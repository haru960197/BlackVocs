from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 
import mongo_utils

app = FastAPI()

@app.get("/")
def test():
    return "Hello World!"

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
    print("Received: ", word)
    inserted_id = mongo_utils.generate_and_insert_item(word)
    return {"message": f"Item '{word}' was saved."}

@app.get("/items/all")
async def read_all_items():
    items = mongo_utils.get_all_items()
    return {"items": items}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=3000, reload=True)
