from typing import Tuple, Any
from datetime import timedelta
from pymongo.database import Database
from repositories.user_repository import UserRepository
from jwt_auth import AuthJwtCsrt
import core.config as config
import core.const as const

class AuthService:
    """Sign-up / sign-in business logic."""
    def __init__(self, db: Database, auth: AuthJwtCsrt | None = None):
        # Inject repository and crypto/JWT provider
        self.users = UserRepository(db, collection_name=config.USER_COLLECTION_NAME)
        self.auth = auth or AuthJwtCsrt()

    # --- Use cases ---
    def signup(self, username: str, email: str, password: str) -> Tuple[str, dict]:
        """
        Create a new user and return (inserted_id, sanitized_user_doc).
        """
        if self.users.exists_username_or_email(username) or self.users.exists_username_or_email(email):
            raise ValueError("Username or email already registered")

        user_doc = {
            "username": username,
            "email": email,
            "full_name": username,
            "hashed_password": self.auth.generate_hashed_pw(password),
            "disabled": False,
        }
        inserted_id = self.users.create(user_doc)

        sanitized = {k: v for k, v in user_doc.items() if k != "hashed_password"}
        sanitized["id"] = inserted_id
        return inserted_id, sanitized

    def signin(self, identifier: str, password: str) -> dict[str, Any]:
        """
        Validate credential and return (user_doc, jwt), username or email.
        """
        user = self.users.find_by_username_or_email(identifier)
        if not user or not self.auth.verify_pw(password, user["hashed_password"]):
            raise ValueError("Incorrect username, email or password")

        # Issue JWT with configured lifetime
        expires = timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = self.auth.encode_jwt(str(user["_id"]), expires_delta=expires)
        return user
