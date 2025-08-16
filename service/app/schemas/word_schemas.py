from pydantic import BaseModel, ConfigDict 
from pydantic.alias_generators import to_camel
from typing import List

class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True)

class ItemBase(CustomBaseModel):
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str 

class ItemCreate(ItemBase): 
    pass

class Item(ItemBase): 
    id: str

class GetUserWordListResponse(BaseModel):
    items: List[Item]
    userid: str

class SuggestWordsRequest(BaseModel): 
    input_word: str
    limit: int = 10 

class SuggestWordsResponse(BaseModel):
    items: List[Item]

class GenerateNewWordEntryRequest(BaseModel): 
    word: str

class GenerateNewWordEntryResponse(BaseModel): 
    item: ItemCreate 

class RegisterWordRequest(BaseModel): 
    item: ItemCreate

class RegisterWordResponse(BaseModel):  
    user_word_id: str

