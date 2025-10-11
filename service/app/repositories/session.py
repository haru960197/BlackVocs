from core.config import MONGO_DB_URL, DB_NAME
from pymongo import MongoClient
from pymongo.database import Database

client = MongoClient(MONGO_DB_URL)

def get_db() -> Database:
    db: Database = client[DB_NAME]
    return db
