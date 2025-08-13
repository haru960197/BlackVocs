from typing import List, Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import core.config as config

USER_WORD_COL = config.USER_WORD_COLLECTION_NAME 

class UserWordRepository:
    """Data access layer for 'user_words' collection."""
    def __init__(self, db: Database, collection_name: str = USER_WORD_COL):
        self.col: Collection = db[collection_name]

    def create_link(self, user_id: ObjectId, word_id: ObjectId) -> str:
        """Create (user_id, word_id) link and return string id."""
        res = self.col.insert_one({"user_id": user_id, "word_id": word_id})
        return str(res.inserted_id)

    def exists_link(self, user_id: ObjectId, word_id: ObjectId) -> bool:
        """Check if the (user, word) link already exists."""
        return self.col.find_one({"user_id": user_id, "word_id": word_id}) is not None

    def list_word_ids_by_user(self, user_id: ObjectId) -> List[ObjectId]:
        """Return word_id list for a given user."""
        cur = self.col.find({"user_id": user_id}, {"word_id": 1})
        return [doc["word_id"] for doc in cur]
