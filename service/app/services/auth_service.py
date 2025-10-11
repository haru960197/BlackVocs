from fastapi import Request
from pymongo.database import Database
from pymongo import errors as mongo_errors
from repositories.user_repository import UserRepository
from core.config import USER_COLLECTION_NAME
from core.errors import (
    ServiceError,
    InvalidCredentialsError,
    ConflictError,
    UnauthorizedError,
    InvalidTokenError, 
    TokenExpiredError, 
)
from models.user import UserInDB
from core.jwt_auth import AuthJwtCsrt

class AuthService:
    def __init__(self, db: Database, auth: AuthJwtCsrt | None = None):
        self.users = UserRepository(db, collection_name=USER_COLLECTION_NAME)
        self.auth = auth or AuthJwtCsrt()

    # --- sign in ---
    def sign_in(self, username: str, password: str) -> str:
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
            user_id = self.users.get_user_id_by_username(username)
            if not user_id: 
                raise InvalidCredentialsError("Incorrect username or password")

            # get hashed password
            hashed_pw = self.users.get_hashed_pw_by_user_id(user_id)
            if not hashed_pw: 
                raise ServiceError("Password is not registered")

            # check if the plaintext password is collect
            if not self.auth.verify_pw(password, hashed_pw): 
                raise InvalidCredentialsError("Incorrect username or password")

            # create token 
            return self.auth.create_access_token(user_id)

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error during deletion: {e}")

    # --- Sign up ---
    def sign_up(self, username: str, password: str) -> str:
        """
        Create a new user and return user_id

        Args: 
            username(str) : new user's username
            password(str) : plaintext password

        Returns: 
            user_id(str) : 
        """
        try: 
            # check if username is not taken 
            if self.users.get_user_id_by_username(username): 
                raise ConflictError("Username is already taken")

            # generate UserInDB model (manage the info in the model between layers(service -> repo))
            user = UserInDB(
                username=username,
                hashed_password=self.auth.generate_hashed_pw(password), 
            )

            # register
            user_id = self.users.create(user)
            if user_id is None: 
                raise ServiceError("Failed to create user: insert returned None")

            return user_id

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error during deletion: {e}")

    # --- check if signed in ---
    @staticmethod
    def get_user_id_from_cookie(request: Request) -> str: 
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


