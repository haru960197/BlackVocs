from typing import List
from pymongo import ReturnDocument
from pymongo.database import Database
from pymongo.collection import Collection
import core.config as config
from core.oid import PyObjectId 
from models.word import WordDetails, WordModel

WORD_COL = config.WORD_COLLECTION_NAME

class WordRepository:
    """Data access layer for 'words' collection."""
    def __init__(self, db: Database, collection_name: str = WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create(self, word_model: WordModel) -> PyObjectId:
        """ insert a new word item """
        doc = word_model.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- read ---
    def find(
        self, 
        *, 
        word_id: PyObjectId | None = None, 
        word_details: WordDetails| None = None,
    ) -> WordModel | None: 
        
        if not word_id and not word_details: 
            raise ValueError("Either word_id or word_base must be provided")

        query = {}
        if word_id is not None: 
            query["_id"] = word_id
        if word_details is not None: 
            query["details"] = word_details.model_dump(by_alias=True, exclude_none=True)

        doc = self.col.find_one(query)
        return WordModel.model_validate(doc) if doc else None

    def find_all(
        self, 
        *, 
        word_ids: List[PyObjectId]
    ) -> List[WordModel]:
        cur = self.col.find({"_id": {"$in": word_ids}})
        return [WordModel.model_validate(doc) for doc in cur]

    def find_by_word_subseq(
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
        cur = self.col.find({"details.spelling": regex}).limit(max_num)
        return [WordModel.model_validate(doc) for doc in cur]

    # --- update ---
    def increment_registration_count(self, word_id: PyObjectId) -> None: 
        self.col.find_one_and_update(
            {"_id": word_id},
            {"$inc": {"registration_count": 1}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )

    def decrement_registration_count(self, word_id: PyObjectId) -> None:
        """
        Decrement registered_count of a word document by word_id
        regisited_count must be greater than 0
        """
        self.col.find_one_and_update(
            {"_id": word_id},
            {"$inc": {"registration_count": -1}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )
