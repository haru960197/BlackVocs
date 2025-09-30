from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ReturnDocument
import core.config as config 
from models.common import PyObjectId, WordBaseModel
from models.word import WordModel

WORD_COL = config.WORD_COLLECTION_NAME

class WordRepository:
    """Data access layer for 'words' collection."""
    def __init__(self, db: Database, collection_name: str = WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create(self, word_base_model: WordBaseModel) -> PyObjectId: 
        """ insert a new word item """
        doc = word_base_model.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- read ---
    def find_model_by_word_id(self, id: PyObjectId) -> WordModel | None: 
        doc = self.col.find_one({"_id": id})
        return WordModel.model_validate(doc) if doc else None

    def find_model_by_word_base_model(self, word_base_model: WordBaseModel) -> WordModel | None: 
        doc = self.col.find_one({"word_base": word_base_model})
        return WordModel.model_validate(doc) if doc else None

    def find_models_by_word_ids(self, word_ids: List[PyObjectId]) -> List[WordModel]:
        """Find words by their IDs and return them as Item list. """
        cur = list(self.col.find({"_id": {"$in": word_ids}}))
        return [WordModel.model_validate(doc) for doc in cur]

    def search_models_by_word_subseq(
        self,
        subseq_pattern: str,
        max_num: int,
        case_insensitive: bool = True
    ) -> List[WordModel]:
        """
        Build a MongoDB regex filter from a subsequence pattern and delegate to regex finder.
        """
        options = "i" if case_insensitive else ""
        regex = {"$regex": subseq_pattern, "$options": options}
        cur = self.col.find({"word_base.word": regex}).limit(max_num)
        return [WordModel.model_validate(doc) for doc in cur]

    def get_registered_count_by_id(self, word_id: PyObjectId) -> int:
        """
        Return the registered_count for a word item by word_id.
        Returns -1 if not found.
        """
        doc = self.col.find_one(
            {"_id": word_id},
            {"registered_count": 1}
        )
        if not doc:
            return -1 

        return int(doc.get("registered_count", 0))

    # --- update ---
    def increment_registered_count(self, word_id: PyObjectId) -> None: 
        self.col.find_one_and_update(
            {"_id": word_id},
            {"$inc": {"registered_count": 1}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )

    def decrement_registered_count(self, word_id: PyObjectId) -> None:
        """
        Decrement registered_count of a word document by word_id
        regisited_count must be greater than 0
        """
        self.col.find_one_and_update(
            {"_id": word_id},
            {"$inc": {"registered_count": -1}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )



