from typing import Optional
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
import core.config as config

USER_COL = config.USER_COLLECTION_NAME 

class UserRepository:
    """Data access layer for users collection."""
    def __init__(self, db: Database, collection_name: str = USER_COL):
        self.col: Collection = db[collection_name]

    # --- Basic CRUD ---
    def create(self, doc: dict) -> str:
        """Insert and return string id."""
        res = self.col.insert_one(doc)
        return str(res.inserted_id)

    def find_by_id(self, _id: str | ObjectId) -> Optional[dict]:
        """Find user by _id."""
        oid = ObjectId(_id) if isinstance(_id, str) else _id
        return self.col.find_one({"_id": oid})

    def find_by_username(self, username: str) -> Optional[dict]:
        """Find user by username."""
        return self.col.find_one({"username": username})

    def exists_username(self, username: str) -> bool:
        """Check if username exists."""
        return self.find_by_username(username) is not None
