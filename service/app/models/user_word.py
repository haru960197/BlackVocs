from pydantic import BaseModel, Field, ConfigDict
from models.common import ExampleBase, PyObjectId

class UserWordModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    user_id: PyObjectId 
    word_id: PyObjectId
    example_base: ExampleBase

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PyObjectId: str},  
    )
