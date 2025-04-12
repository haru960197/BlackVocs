# start application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
import uvicorn 
import mongo_utils
import config
from typing import List

app = FastAPI()

# ミドルウェアでCORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.WEB_URI],  # Next.jsのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test():
    return "Hello World!"


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    

class Item(CustomBaseModel):
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str


class InsertItemRequest(CustomBaseModel):
    item: Item

class InsertNewWordRequest(CustomBaseModel):
    word: str


# POSTで受け取ったItemをMongoDBに保存
@app.post("/dictionary")
async def insert_item(request: InsertItemRequest):
    item = request.item
    print("Received: ", item)
    inserted_id = mongo_utils.insert_item(item)  # Mongoに保存
    return {"message": f"Item '{item.name}' was saved.", "id": inserted_id}

@app.post("/new_word")
async def insert_new_word(request: InsertNewWordRequest):
    """
    単語からitemを生成し，データベースに保存
    """
    word = request.word
    print("Received: ", word)
    inserted_id = mongo_utils.generate_and_insert_item(word)
    return {"message": f"Item '{word}' was saved."}

@app.get("/items/all", response_model=List[Item])
async def read_all_items():
    items = mongo_utils.get_all_items()
    return {"items": items}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=config.SERVICE_PORT, reload=True)
