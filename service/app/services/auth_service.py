from fastapi import Request
from pymongo.database import Database
from pymongo import errors as mongo_errors
from repositories.user_repository import UserRepository
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
from schemas.auth_schemas import SignInRequest, SignUpRequest

class AuthService:
    def __init__(self, db: Database):
        self.users = UserRepository(db)
        self.auth = AuthJwtCsrt()

    # --- sign in ---
    def create_access_token(self, payload: SignInRequest) -> str:
        """
        Authenticate a user with the given username and plaintext password
        return access token
        """
        try: 
            # check if user exists
            user = self.users.find(username=payload.username)
            if not user: 
                raise NotFoundError("given username is not in DB")

            # check if the plaintext password is collect
            if not self.auth.verify_pw(payload.password, user.hashed_password): 
                raise InvalidCredentialsError("Incorrect password")

            # create token 
            if user.id is None: 
                raise ServiceError("failed to get user id")
            return self.auth.encode_jwt(user.id)

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error during deletion: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

    # --- Sign up ---
    def sign_up(self, payload: SignUpRequest) -> None:
        """
        Create a new user and return user_id
        """
        try: 
            # check if username is not taken 
            if self.users.find(username=payload.username): 
                raise ConflictError("Username is already taken")

            new_user_model = UserModel(
                username=payload.username,
                hashed_password=self.auth.generate_hashed_pw(payload.password), 
            )

            # register
            user_id = self.users.create(new_user_model)
            if user_id is None: 
                raise ServiceError("Failed to create user: insert returned None")

            return 

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error during deletion: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

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
        except Exception as e:
            raise ServiceError(f"service error: {e}")


