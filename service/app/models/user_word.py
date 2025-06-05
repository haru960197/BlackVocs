from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from models.common import PyObjectId

class UserWordModel(BaseModel):
    """
    Container for a user-word record
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str 
    word_id: str 

    class Config:
        allow_population_by_field_name = True  
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
