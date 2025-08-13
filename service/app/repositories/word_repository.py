from typing import Optional, List
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import core.config as config 

WORD_COL = config.WORD_COLLECTION_NAME

class WordRepository:
    """Data access layer for 'words' collection."""
    def __init__(self, db: Database, collection_name: str = WORD_COL):
        self.col: Collection = db[collection_name]

    def create(self, doc: dict) -> str:
        """Insert a word document and return its string id."""
        res = self.col.insert_one(doc)
        return str(res.inserted_id)

    def find_by_id(self, _id: str | ObjectId) -> Optional[dict]:
        """Find a word by _id."""
        oid = ObjectId(_id) if isinstance(_id, str) else _id
        return self.col.find_one({"_id": oid})

    def find_by_word_exact(self, word: str, case_insensitive: bool = True) -> Optional[dict]:
        """Find a word by exact spelling."""
        if case_insensitive:
            return self.col.find_one({"word": {"$regex": f"^{word}$", "$options": "i"}})
        return self.col.find_one({"word": word})

    def find_by_ids(self, ids: List[str]) -> List[dict]:
        """Find many words by id list."""
        oids = [ObjectId(i) for i in ids]
        return list(self.col.find({"_id": {"$in": oids}}))

    def find_prefix(self, q: str, limit: int = 10, case_insensitive: bool = True, exclude_ids: list[ObjectId] | None = None) -> List[dict]:
        """Prefix search with optional exclusions."""
        filt: dict = {"word": {"$regex": f"^{q}", "$options": "i" if case_insensitive else ""}}
        if exclude_ids:
            filt = {"$and": [filt, {"_id": {"$nin": exclude_ids}}]}
        return list(self.col.find(filt).sort("word", 1).limit(limit))
