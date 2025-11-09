from pydantic import BaseModel, ConfigDict, conint, Field
from core.oid import PyObjectId

class WordDetails(BaseModel): 
    spelling: str
    meaning: str | None

class WordModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    details: WordDetails
    registration_count: conint(ge=0) = 0 

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PyObjectId: str},
    )

