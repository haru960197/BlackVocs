from typing import Optional
from pydantic import BaseModel
from typing import List


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