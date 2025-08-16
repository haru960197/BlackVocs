from urllib import parse
from core.config import MONGO_DB_URL
from pymongo import MongoClient
from pymongo.database import Database

client = MongoClient(MONGO_DB_URL)

def get_db() -> Database:
    db: Database = client.db
    return db
