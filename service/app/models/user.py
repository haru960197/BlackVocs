from pydantic import BaseModel, EmailStr
from typing import Optional

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str
    disabled: bool = False