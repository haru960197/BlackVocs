from pydantic import BaseModel, Field
from models.common import PyObjectId

class User(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    username: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str
