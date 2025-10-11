from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId #type: ignore
import core.config as config

USER_WORD_COL = config.USER_WORD_COLLECTION_NAME 

class UserWordRepository:
    def __init__(self, db: Database, collection_name: str = USER_WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create_link(self, user_id: str, word_id: str) -> str:
        """Create (user_id, word_id) link and return string id."""
        res = self.col.insert_one({"user_id": ObjectId(user_id), "word_id": ObjectId(word_id)})
        return str(res.inserted_id)

    # --- read ---
    def get_word_ids_by_user_id(self, user_id: str) -> List[str]:
        """Return word_id list for a given user."""
        cur = self.col.find({"user_id": ObjectId(user_id)}, {"word_id": 1, "_id": 0})
        return [str(doc["word_id"]) for doc in cur]

    def get_link(self, user_id: str, word_id: str) -> str | None:
        """ 
        check if (user_id, word_id) is in the user_word_collection 
        if exist: return id 
        else: return None
        """
        doc = self.col.find_one(
            {
                "user_id": ObjectId(user_id),
                "word_id": ObjectId(word_id),
            },
            {"_id": 1}  
        )
        return str(doc["_id"]) if doc else None

    # --- delete ---
    def delete_link(self, user_id: str, word_id: str) -> str | None: 
        doc = self.col.find_one_and_delete(
            {
                "user_id": ObjectId(user_id),
                "word_id": ObjectId(word_id),
            },
            projection={"_id": 1},  
        )

        return str(doc["_id"]) if doc else None

