import re
from pydantic import BaseModel, Field

from core import const

# --- sign in ---
class SignInRequest(BaseModel):
    username: str = Field(
        min_length=const.USERNAME_MIN_LEN, 
        max_length=const.USERNAME_MAX_LEN,
    )
    password: str = Field(
        min_length=const.PASSWORD_MIN_LEN, 
        max_length=const.PASSWORD_MAX_LEN, 
        pattern=re.compile(const.PASSWORD_REGEX_PATTERN), 
    )

class SignInResponse(BaseModel):
    access_token: str

# --- sign up ---
class SignUpRequest(BaseModel):
    username: str = Field(
        min_length=const.USERNAME_MIN_LEN, 
        max_length=const.USERNAME_MAX_LEN,
    )
    password: str = Field(
        min_length=const.PASSWORD_MIN_LEN, 
        max_length=const.PASSWORD_MAX_LEN, 
        pattern=re.compile(const.PASSWORD_REGEX_PATTERN), 
    )

# --- check if signed in ---
class SignedInCheckResponse(BaseModel):
    user_id: str 
