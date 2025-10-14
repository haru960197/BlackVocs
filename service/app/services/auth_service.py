from fastapi import Request
from pymongo.database import Database
from pymongo import errors as mongo_errors
from repositories.user_repository import UserRepository
from core.config import USER_COLLECTION_NAME
from core.errors import (
    NotFoundError,
    ServiceError,
    InvalidCredentialsError,
    ConflictError,
    UnauthorizedError,
    InvalidTokenError, 
    TokenExpiredError, 
)
from core.jwt_auth import AuthJwtCsrt
from core.oid import PyObjectId
from models.user import UserModel

class AuthService:
    def __init__(self, db: Database, auth: AuthJwtCsrt | None = None):
        self.users = UserRepository(db, collection_name=USER_COLLECTION_NAME)
        self.auth = auth or AuthJwtCsrt()

    # --- sign in ---
    def sign_in(self, username: str, plaintext_password: str) -> str:
        """
        Authenticate a user with the given username and password

        Args: 
            username(str) : username used for login 
            password(str) : Plaintext password

        Returns: 
            token(str) : access token 
        """
        try: 
            # check if user exists
            user = self.users.find_user(username=username)
            if not user: 
                raise NotFoundError("given username is not in DB")

            # check if the plaintext password is collect
            if not self.auth.verify_pw(plaintext_password, user.hashed_password): 
                raise InvalidCredentialsError("Incorrect password")

            # create token 
            if user.id is None: 
                raise ServiceError("failed to get user id")
            return self.auth.create_access_token(user.id)

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error during deletion: {e}")

    # --- Sign up ---
    def sign_up(self, username: str, plaintext_password: str) -> PyObjectId:
        """
        Create a new user and return user_id

        Args: 
            username(str) : new user's username
            password(str) : plaintext password

        Returns: 
            user_id(PyObjectId) : 
        """
        try: 
            # check if username is not taken 
            if self.users.find_user(username=username): 
                raise ConflictError("Username is already taken")

            # generate usermodel
            user = UserModel(
                username=username,
                hashed_password=self.auth.generate_hashed_pw(plaintext_password), 
            )

            # register
            user_id = self.users.create_user(user)
            if user_id is None: 
                raise ServiceError("Failed to create user: insert returned None")

            return user_id

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error during deletion: {e}")

    # --- check if signed in ---
    @staticmethod
    def get_user_id_from_cookie(request: Request) -> PyObjectId: 
        """get user_id from cookie, return user_id """
        try: 
            auth = AuthJwtCsrt()

            # get token
            token = request.cookies.get("access_token")
            if token is None:
                raise UnauthorizedError("Access token is missing in cookies")
            if token.startswith("Bearer "):
                token = token[7:]
            
            # decode token
            return auth.decode_jwt(token=token)

        except (InvalidTokenError, TokenExpiredError) as e: 
            raise UnauthorizedError(str(e))


