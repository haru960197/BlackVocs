from pydantic import BaseModel, Field, ConfigDict
from core.oid import PyObjectId

class UserModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    username: str
    hashed_password: str
    disabled: bool = False

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PyObjectId: str},  
    )
