from typing import Optional
from pydantic import BaseModel
from typing import List, Union


# フロントから送られる型
class UserBody(BaseModel):
    email: str
    password: str

# 複数のエンドポイントで使う
class UserInfo(BaseModel):
    id: Optional[str] = None # Optionalで任意の値
    email: str

# emailのリストを集めるときに使う(for testing)
class UserPublic(BaseModel):
    id: str
    email: str

class GetAllUsersResponse(BaseModel):
    users: List[UserPublic]

# user --------------------------------------
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

# token -------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None