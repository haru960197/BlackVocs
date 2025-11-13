from pydantic import BaseModel, Field, ConfigDict
from core.oid import PyObjectId

class UsageExample(BaseModel): 
    sentence: str | None = None
    translation: str | None = None

class UserWordModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    user_id: PyObjectId 
    word_id: PyObjectId
    usage_example: UsageExample 

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PyObjectId: str},  
    )
