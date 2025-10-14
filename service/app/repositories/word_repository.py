from typing import List
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ReturnDocument
import core.config as config 
from core.oid import PyObjectId
from models.common import WordBaseModel
from models.word import WordModel

WORD_COL = config.WORD_COLLECTION_NAME

class WordRepository:
    """Data access layer for 'words' collection."""
    def __init__(self, db: Database, collection_name: str = WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create_word(self, word_model: WordModel) -> PyObjectId: 
        """ insert a new word item """
        doc = word_model.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- read ---
    def find_word(
        self, 
        word_id: PyObjectId | None = None, 
        word_base: WordBaseModel | None = None,
    ): 
        
        if not word_id and not word_base: 
            raise ValueError("Either word_id or word_base must be provided")

        if word_id: 
            doc = self.col.find_one({"_id": word_id})
            return WordModel.model_validate(doc) if doc else None

        if word_base: 
            query = {"word_base": word_base.model_dump(by_alias=True, exclude_none=True)}
            doc = self.col.find_one(query)
            return WordModel.model_validate(doc) if doc else None

    def find_words_by_word_subseq(
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
