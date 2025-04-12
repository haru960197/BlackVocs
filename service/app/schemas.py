from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

# words
class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True)

class Item(CustomBaseModel):
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str 

class AddNewWordRequest(CustomBaseModel):
    item: Item

class AddNewWordResponse(CustomBaseModel):
    item: Item

class GetAllItemsResponse(CustomBaseModel):
    items: List[Item]


# DB
class DBConfig(BaseSettings):
    DB_USERNAME: str = Field(description="DBのユーザ名")
    DB_PASSWORD: str = Field(description="DBのパスワード")
    DB_HOST: str = Field(description="DBのホスト名")
    DB_PORT: str = Field(description="DBのポート番号")