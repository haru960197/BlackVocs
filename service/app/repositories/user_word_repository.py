from pymongo.database import Database
from pymongo.collection import Collection
import core.config as config
from core.oid import PyObjectId
from models.user_word import UserWordModel

USER_WORD_COL = config.USER_WORD_COLLECTION_NAME 

class UserWordRepository:
    def __init__(self, db: Database, collection_name: str = USER_WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create_user_word(self, user_word_model: UserWordModel) -> PyObjectId:
        """Create (user_id, word_id) link and return string id."""
        doc = user_word_model.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- read ---
    def find_user_word(
        self, 
        user_id: PyObjectId, 
        word_id: PyObjectId | None = None, 
    ):
        """Find user_word based on user_id and word_id."""
        query = {"user_id": user_id}
        if word_id is None: 
            cur = self.col.find(query)
            return [UserWordModel.model_validate(doc) for doc in cur]

        query["word_id"] = word_id
        doc = self.col.find_one(query)
        return UserWordModel.model_validate(doc) if doc else None

    # --- delete ---
    def delete_user_word(self, user_word_id: PyObjectId) -> UserWordModel | None: 
        doc = self.col.find_one_and_delete({"_id": user_word_id})
        return UserWordModel.model_validate(doc) if doc else None

