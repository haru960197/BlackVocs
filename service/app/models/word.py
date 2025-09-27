from pydantic import BaseModel, ConfigDict, conint, Field
from models.common import WordBaseModel, PyObjectId

class WordModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    word_base: WordBaseModel
    register_count: conint(ge=0)  

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PyObjectId: str},
    )
