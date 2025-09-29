from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
import core.config as config
from models.common import PyObjectId
from models.user_word import UserWordModel

USER_WORD_COL = config.USER_WORD_COLLECTION_NAME 

class UserWordRepository:
    def __init__(self, db: Database, collection_name: str = USER_WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create(self, user_id: PyObjectId, word_id: PyObjectId) -> PyObjectId:
        """Create (user_id, word_id) link and return string id."""
        res = self.col.insert_one({"user_id": user_id, "word_id": word_id})
        return res.inserted_id

    # --- read ---
    def find_models_by_user_id(self, user_id: PyObjectId) -> List[UserWordModel]:
        """ return user_word models by user id """
        cur = self.col.find({"user_id": user_id})
        return [UserWordModel.model_validate(doc) for doc in cur]

    def find_word_ids_by_user_id(self, user_id: PyObjectId) -> List[PyObjectId]:
        """Return word_id list for a given user."""
        cur = self.col.find({"user_id": user_id}, {"word_id": 1})
        return [doc["word_id"] for doc in cur]

    def find_link(self, user_id: PyObjectId, word_id: PyObjectId) -> PyObjectId | None:
        """ 
        check if (user_id, word_id) is in the user_word_collection 
        if exist: return id 
        else: return None
        """
        doc = self.col.find_one(
            {
                "user_id": user_id,
                "word_id": word_id,
            },
            {"_id": 1}  
        )
        return doc["_id"] if doc else None

    # --- delete ---
    def delete_link(self, user_id: PyObjectId, word_id: PyObjectId) -> PyObjectId | None: 
        doc = self.col.find_one_and_delete(
            {
                "user_id": user_id,
                "word_id": word_id,
            },
            projection={"_id": 1},  
        )

        return doc["_id"] if doc else None

