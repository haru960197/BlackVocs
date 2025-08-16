from typing import List, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ReturnDocument
from bson import ObjectId # type: ignore
import core.config as config 
from models.word import Item, Entry 
from utils.fingerprint import entry2fingerprint

WORD_COL = config.WORD_COLLECTION_NAME

class WordRepository:
    """Data access layer for 'words' collection."""
    def __init__(self, db: Database, collection_name: str = WORD_COL):
        self.col: Collection = db[collection_name]

    # --- find by ---
    def find_by_fingerprint(self, fpr: str) -> str | None: 
        doc = self.col.find_one({"fingerprint": fpr}, {"_id": 1})
        return str(doc["_id"]) if doc else None

    def find_by_entry(self, entry: Entry) -> str | None: 
        """ if an Entry is in DB, return ID, else return None """
        fpr = entry2fingerprint(entry)
        return self.find_by_fingerprint(fpr)

    def find_by_ids(self, word_ids: List[str]) -> List[Item]:
        """Find words by their IDs and return them as Item list (not Entry). """
        if not word_ids:
            return []

        object_ids = [ObjectId(wid) for wid in word_ids]
        docs = list(self.col.find({"_id": {"$in": object_ids}}))
        ret = [Item.model_validate(doc) for doc in docs]
        print(ret)
        return ret

    # --- add ---
    def upsert_and_inc_entry(self, entry: Entry) -> str:
        fpr = entry2fingerprint(entry)
        
        updated = self.col.find_one_and_update(
            {"fingerprint": fpr},
            {
                "$setOnInsert": { 
                    "entry": entry.model_dump(), 
                    "fingerprint": fpr, 
                },
                "$inc": {"registered_count": 1}, 
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )
        return str(updated["_id"])

    def find_candidates_by_entry_word_regex(
        self,
        regex_filter: Dict[str, Any],
        limit: int
    ) -> List[Item]:
        """
        Find candidate words by applying a MongoDB regex filter to 'entry.word'.
        """
        cursor = self.col.find({"entry.word": regex_filter}).limit(int(limit))
        return [Item.model_validate(doc) for doc in cursor]

    def find_candidates_by_entry_word_subsequence(
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
        return self.find_candidates_by_entry_word_regex(regex, limit)
