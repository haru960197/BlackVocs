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
    def create_user(self, user: UserModel) -> PyObjectId:
        """Insert a new user item"""
        doc = user.model_dump(by_alias=True, exclude_none=True)
        res = self.col.insert_one(doc)
        return res.inserted_id

    # --- read ---
    def find_user(
        self,
        user_id: PyObjectId | None = None,
        username: str | None = None,
        projection: dict | None = None,
    ) -> UserModel | None:

        if not user_id and not username:
            raise ValueError("Either user_id or username must be provided")

        query = {"_id": user_id} if user_id else {"username": username}

        doc = self.col.find_one(query, projection)
        return UserModel.model_validate(doc) if doc else None
