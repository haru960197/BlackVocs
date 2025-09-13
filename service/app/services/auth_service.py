from typing import Any
from pymongo.database import Database
from pymongo import errors as mongo_errors
from repositories.user_repository import UserRepository
from core.config import USER_COLLECTION_NAME
from core.errors import (
    ServiceError,
    InvalidCredentialsError,
    AuthenticationBackendError, 
    ConflictError,
)
from core.jwt_auth import AuthJwtCsrt

class AuthService:
    def __init__(self, db: Database, auth_util: AuthJwtCsrt | None = None):
        self.users = UserRepository(db, collection_name=USER_COLLECTION_NAME)
        self.auth = auth_util or AuthJwtCsrt()

    # --- sign in ---
    def sign_in(self, identifier: str, password: str) -> dict[str, Any]:
        """
        Validate credential and return (user_doc, jwt), username or email.
        """
        if not identifier or not password:
            raise InvalidCredentialsError("Incorrect username, email or password")

        try: 
            user = self.users.find_by_username_or_email(identifier)
        except mongo_errors.PyMongoError as e:
            raise AuthenticationBackendError("Auth datastore error") from e

        if not user: 
            raise InvalidCredentialsError("Incorrect username, email or password")

        try: 
            ok = self.auth.verify_pw(password, user["hashed_password"])
        except Exception as e:
            raise AuthenticationBackendError("Password verification failed") from e

        if not ok:
            raise InvalidCredentialsError("Incorrect username, email or password")

        return user

    # --- Sign up ---
    def signup(self, username: str, email: str, password: str) -> str:
        """
        Create a new user and return (inserted_id, sanitized_user_doc).
        """
        if not username or not email or not password:
            raise ServiceError("Missing required fields")

        try: 
            if self.users.find_by_username_or_email(username):
                raise ConflictError("Username/email is already taken")
            if self.users.find_by_username_or_email(email): 
                raise ConflictError("Username/email is already taken")
        except mongo_errors.PyMongoError as e:
            raise AuthenticationBackendError("Auth datastore error") from e

        try: 
            hashed = self.auth.generate_hashed_pw(password)
            doc = {
                "username": username,
                "email": email,
                "hashed_password": hashed 
            }
            inserted_id = self.users.create(doc)
        except mongo_errors.PyMongoError as e: 
            raise AuthenticationBackendError("Failed to create user") from e
        except Exception as e:
            raise ServiceError("Failed to create user") from e

        return inserted_id

