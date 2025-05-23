from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

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
    word: str

class AddNewWordResponse(CustomBaseModel):
    user_word_id: str 
