from pymongo import MongoClient
from pydantic import BaseModel
import config

# 型定義
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

def connect_to_mongodb(uri=config.DB_URI):
    client = MongoClient(uri)
    return client[config.DB_NAME][config.COLLECTION_NAME]  # "items" コレクション使用

def insert_item(item: Item):
    collection = connect_to_mongodb()
    result = collection.insert_one(item.dict())  # pydanticモデル → dict
    print(f"[Insert] ID: {result.inserted_id}")
    return str(result.inserted_id)

def get_all_items():
    collection = connect_to_mongodb()
    items = list(collection.find({}, {"_id": 0}))  # _idを除外して取得
    return items