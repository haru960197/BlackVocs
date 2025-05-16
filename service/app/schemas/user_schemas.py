from pydantic import BaseModel, EmailStr
from typing import Union

# user --------------------------------------
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# token -------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# login -------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str