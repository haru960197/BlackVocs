from typing import Any, List
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
    def create(self, user_word_model: UserWordModel) -> PyObjectId:
        """Create (user_id, word_id) link and return id."""
        doc = user_word_model.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- update --- 
    def update(self, user_word_id: PyObjectId, update_doc: dict[str, Any]) -> int: 
        query = {"_id": user_word_id}
        update_operation = {"$set": update_doc}
        res = self.col.update_one(query, update_operation)
        return res.modified_count

    # --- read ---
    def find(
        self, 
        *, 
        user_word_id: PyObjectId | None = None,
        user_id: PyObjectId | None = None, 
        word_id: PyObjectId | None = None, 
    ) -> UserWordModel | None:
        """ find a user_word matching to the condition """
        if user_word_id is not None: 
            query = {"_id": user_word_id}
            doc = self.col.find_one(query)
            return UserWordModel.model_validate(doc) if doc else None

        if not (user_id and word_id): 
            raise ValueError("both user_id and word_id must be provided")

        query = {"user_id": user_id, "word_id": word_id}
        doc = self.col.find_one(query)
        return UserWordModel.model_validate(doc) if doc else None

    def find_all(
        self, 
        *,
        user_id: PyObjectId | None = None, 
        word_id: PyObjectId | None = None
    ) -> List[UserWordModel]:
        """ find user_word list matching to the condition """

        if not user_id and not word_id: 
            raise ValueError("either user_id and word_id must be provided")

        query = {}
        if user_id is not None: 
            query["user_id"] = user_id
        if word_id is not None: 
            query["word_id"] = word_id
            
        cur = self.col.find(query)
        return [UserWordModel.model_validate(doc) for doc in cur]

    # --- delete ---
    def delete(self, user_word_id: PyObjectId) -> UserWordModel | None: 
        doc = self.col.find_one_and_delete({"_id": user_word_id})
        return UserWordModel.model_validate(doc) if doc else None

