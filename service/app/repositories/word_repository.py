from typing import Optional, List
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ReturnDocument
from bson import ObjectId # type: ignore
import core.config as config 
from models.word import Item, Entry 
from utils.fingerprint import entry2fingerprint
from pymongo.errors import DuplicateKeyError

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

    def add_new_entry(self, entry: Entry) -> str | None:
        """Insert a new Item built from Entry and return its _id as string."""

        fpr = entry2fingerprint(entry)
        item = Item(entry=entry, fingerprint=fpr)  

        doc = item.model_dump(by_alias=True)

        try: 
            result = self.col.insert_one(doc)
            return str(result.inserted_id)
        except DuplicateKeyError: 
            existing = self.col.find_one({"fingerprint": fpr}, {"_id": 1})
            if existing:
                return str(existing["_id"])
            raise

    def inc_registered_count(self, oid: str, amount: int = 1) -> str:
        """Increment registered_count for a given _id."""
        updated = self.col.find_one_and_update(
            {"_id": ObjectId(oid)},
            {"$inc": {"registered_count": amount}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 1},
        )
        if not updated:
            raise ValueError(f"No document found with _id={oid}")
        return str(updated["_id"])



