from typing import List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId #type: ignore
import core.config as config

USER_WORD_COL = config.USER_WORD_COLLECTION_NAME 

class UserWordRepository:
    def __init__(self, db: Database, collection_name: str = USER_WORD_COL):
        self.col: Collection = db[collection_name]

    def create_link(self, user_id: str, word_id: str) -> str:
        """Create (user_id, word_id) link and return string id."""
        res = self.col.insert_one({"user_id": ObjectId(user_id), "word_id": ObjectId(word_id)})
        return str(res.inserted_id)

    def exists_link(self, user_id: str, word_id: str) -> bool:
        return self.col.find_one({
            "user_id": ObjectId(user_id),
            "word_id": ObjectId(word_id)
        }) is not None

    def list_word_ids_by_user(self, user_id: str) -> List[str]:
        """Return word_id list for a given user."""
        cur = self.col.find({"user_id": ObjectId(user_id)}, {"word_id": 1, "_id": 0})
        return [str(doc["word_id"]) for doc in cur]
