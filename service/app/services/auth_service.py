from typing import Tuple
from pymongo.database import Database
from passlib.context import CryptContext
from repositories.user_repository import UserRepository
import core.config as config

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Sign-up/sign-in business logic."""
    def __init__(self, db: Database):
        self.users = UserRepository(db, collection_name=config.USER_COLLECTION_NAME)

    # --- Password helpers ---
    def hash_password(self, plain: str) -> str:
        """Hash plaintext password."""
        return pwd_ctx.hash(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verify plaintext vs hashed password."""
        return pwd_ctx.verify(plain, hashed)

    # --- Use cases ---
    def signup(self, username: str, email: str, password: str) -> Tuple[str, dict]:
        """
        Create a new user and return (inserted_id, user_doc_without_password).
        """
        if self.users.exists_username(username):
            raise ValueError("Username already registered")

        user_doc = {
            "username": username,
            "email": email,
            "full_name": username,
            "hashed_password": self.hash_password(password),
            "disabled": False,
        }
        inserted_id = self.users.create(user_doc)
        # remove secrets for return
        user_doc_sanitized = {k: v for k, v in user_doc.items() if k != "hashed_password"}
        user_doc_sanitized["_id"] = inserted_id
        return inserted_id, user_doc_sanitized

    def signin(self, username: str, password: str) -> dict:
        """
        Validate credential and return user_doc.
        """
        user = self.users.find_by_username(username)
        if not user or not self.verify_password(password, user["hashed_password"]):
            raise ValueError("Incorrect username or password")
        return user
