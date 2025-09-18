from typing import List, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ReturnDocument
from bson import ObjectId 
import core.config as config 
from models.word import Item, Entry 

WORD_COL = config.WORD_COLLECTION_NAME

class WordRepository:
    """Data access layer for 'words' collection."""
    def __init__(self, db: Database, collection_name: str = WORD_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create_item(self, fpr: str, entry: Entry) -> str: 
        """ insert a new word item """
        doc: Dict[str, Any] = {
            "fingerprint": fpr,
            "entry": entry.model_dump(),
            "registered_count": 0,  # initialize with 0
        }
        res = self.col.insert_one(doc)
        return str(res.inserted_id)

    # --- read ---
    def exists_word_id(self, word_id: str) -> bool: 
        doc = self.col.find_one({"_id": ObjectId(word_id)})
        return doc is not None

    def get_items_by_word_ids(self, word_ids: List[str]) -> List[Item]:
        """Find words by their IDs and return them as Item list. """
        object_ids = [ObjectId(wid) for wid in word_ids]
        docs = list(self.col.find({"_id": {"$in": object_ids}}))
        return [Item.model_validate(doc) for doc in docs]

    def get_items_by_word_subseq(
        self,
        subseq_pattern: str,
        limit: int,
        case_insensitive: bool = True
    ) -> List[Item]:
        """
        Build a MongoDB regex filter from a subsequence pattern and delegate to regex finder.
        """
        options = "i" if case_insensitive else ""
        regex = {"$regex": subseq_pattern, "$options": options}
        docs = self.col.find({"entry.word": regex}).limit(limit)
        return [Item.model_validate(doc) for doc in docs]

    def get_id_by_fpr(self, fpr: str) -> str | None: 
        """ Find word by fingerprint, return id, if not exist, return None """ 
        doc = self.col.find_one({"fingerprint": fpr}, {"_id": 1})
        return str(doc["_id"]) if doc else None

    def get_registered_count_by_id(self, word_id: str) -> int:
        """
        Return the registered_count for a word item by word_id.
        Returns -1 if not found.
        """
        doc = self.col.find_one(
            {"_id": ObjectId(word_id)},
            {"registered_count": 1}
        )
        if not doc:
            return -1 

        return int(doc.get("registered_count", 0))

    # --- update ---
    def increment_registered_count(self, word_id: str) -> None: 
        self.col.find_one_and_update(
            {"_id": ObjectId(word_id)},
            {"$inc": {"registered_count": 1}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )

    def decrement_registered_count(self, word_id: str) -> None:
        """
        Decrement registered_count of a word document by word_id
        regisited_count must be greater than 0
        """
        self.col.find_one_and_update(
            {"_id": ObjectId(word_id)},
            {"$inc": {"registered_count": -1}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )



