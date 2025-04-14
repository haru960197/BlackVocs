from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

# words
class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True)

class Item(CustomBaseModel):
    id: str
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str 

class AddNewWordRequest(CustomBaseModel):
    word: str

class AddNewWordResponse(CustomBaseModel):
    item: Item

class GetAllItemsResponse(CustomBaseModel):
    items: List[Item]

