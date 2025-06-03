from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class TokenData(BaseModel):
    username: str | None = None