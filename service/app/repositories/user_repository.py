from typing import Optional, Dict, Any
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

    def find_by_id(self, _id: str | ObjectId) -> dict[str, Any] | None:
        """Find user by _id."""
        oid = ObjectId(_id) if isinstance(_id, str) else _id
        return self.col.find_one({"_id": oid})

    def find_by_username_or_email(self, identifier: str) -> dict[str, Any] | None:
        """Find user by username or email."""
        return self.col.find_one(
            {"$or": [{"username": identifier}, {"email": identifier}]}
        )

    def exists_username_or_email(self, identifier: str) -> bool: 
        """Check if username or email exists."""
        return self.find_by_username_or_email(identifier) is not None
