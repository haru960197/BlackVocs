from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from models.common import PyObjectId

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class TokenData(BaseModel):
    username: str | None = None
