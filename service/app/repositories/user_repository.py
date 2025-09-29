from pymongo.database import Database
from pymongo.collection import Collection
import core.config as config
from models.user import UserModel 
from models.common import PyObjectId

USER_COL = config.USER_COLLECTION_NAME 

class UserRepository:
    """Data access layer for users collection."""
    def __init__(self, db: Database, collection_name: str = USER_COL):
        self.col: Collection = db[collection_name]

    # --- create ---
    def create(self, user: UserModel) -> PyObjectId:
        """Insert a new user item"""
        doc = user.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- read ---
    def find_user_id_by_username(self, username: str) -> PyObjectId | None: 
        """find user by username, return user_id(exists) or None(not exist)""" 
        doc = self.col.find_one({"username": username}, {"_id": 1})
        return doc["_id"] if doc else None

    def find_hashed_pw_by_user_id(self, user_id: PyObjectId) -> str | None: 
        """find user's hashed password, return it or None(exist)"""
        doc = self.col.find_one({"_id": user_id}, {"hashed_password": 1})
        return doc["hashed_password"] if doc else None

