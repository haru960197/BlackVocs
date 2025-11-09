from pydantic import BaseModel, field_validator
from typing import List

# --- get user word list ---
class GetUserWordListResponseBase(BaseModel):
    user_word_id: str 
    spelling: str 
    meaning: str | None = None
    example_sentence: str | None = None
    example_sentence_translation: str | None = None

    @field_validator("spelling")
    def to_lowercase(cls, v: str) -> str:
        return v.strip().lower()

class GetUserWordListResponse(BaseModel):
    word_list: List[GetUserWordListResponseBase]

# --- suggest ---
class SuggestWordsRequest(BaseModel): 
    input_str: str
    max_num: int = 10 

class SuggestWordsResponseBase(BaseModel): 
    word_id: str
    spelling: str 
    meaning: str | None = None 

class SuggestWordsResponse(BaseModel):
    word_list: List[SuggestWordsResponseBase]

# --- generate ---
class GenerateNewWordEntryRequest(BaseModel): 
    spelling: str 
    meaning: str | None = None
    example_sentence: str | None = None
    example_sentence_translation: str | None = None

class GenerateNewWordEntryResponse(BaseModel): 
    spelling: str 
    meaning: str
    example_sentence: str
    example_sentence_translation: str

# --- register word ---
class RegisterWordRequest(BaseModel): 
    spelling: str 
    meaning: str | None = None
    example_sentence: str | None = None
    example_sentence_translation: str | None = None

class RegisterWordResponse(BaseModel):  
    user_word_id: str

# --- delete ---
class DeleteWordRequest(BaseModel): 
    user_word_id: str

