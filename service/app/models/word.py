from pydantic import BaseModel, Field
from typing import Optional
from models.common import PyObjectId
from bson import ObjectId 

class Entry(BaseModel):
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str

class Item(BaseModel):
    id: ObjectId = Field(alias = "_id", default=None)
    entry: Entry 
    fingerprint: str = Field(..., description = "deterministic fingerprint for enties")
    registered_count: int = Field(default = 0, ge = 0, description = "Number of users who registered this word")

    class Config:
        populate_by_name = True 
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
