from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List

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
    item: Item
    user_word_id: str

class GetUserWordListResponse(BaseModel):
    wordlist: List[Item]
    userid: str

class SuggestWordsResponse(BaseModel):
    items: List[Item]

class GenerateNewWordEntryRequest(BaseModel): 
    word: str

class GenerateNewWordEntryResponse(BaseModel): 
    item: Item 

