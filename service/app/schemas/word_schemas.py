from pydantic import BaseModel, Field, field_validator
from typing import List

from core import const

# --- get user word list ---
class GetWordListResponseBase(BaseModel):
    user_word_id: str 
    spelling: str
    meaning: str | None = None 

class GetWordListResponse(BaseModel):
    word_list: List[GetWordListResponseBase]

# --- user word detail --- 
class GetWordContentRequest(BaseModel): 
    user_word_id: str

class GetWordContentResponse(BaseModel): 
    user_word_id: str
    spelling: str 
    meaning: str | None = None
    example_sentence: str | None = None
    example_sentence_translation: str | None = None 

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
    spelling: str = Field(
        min_length=const.SPELLING_MIN_LEN,
        max_length=const.SPELLING_MAX_LEN, 
    )
    meaning: str | None = Field(
        max_length=const.MEANING_MAX_LEN,
    )
    example_sentence: str | None = Field(
        max_length=const.EXAMPLE_MAX_LEN,
    )
    example_sentence_translation: str | None = Field(
        max_length=const.EXAMPLE_TRANSLATION_MAX_LEN, 
    )

class GenerateNewWordEntryResponse(BaseModel): 
    spelling: str 
    meaning: str
    example_sentence: str
    example_sentence_translation: str

# --- register word ---
class RegisterWordRequest(BaseModel): 
    spelling: str = Field(
        min_length=const.SPELLING_MIN_LEN,
        max_length=const.SPELLING_MAX_LEN, 
    )
    meaning: str | None = Field(
        max_length=const.MEANING_MAX_LEN,
    )
    example_sentence: str | None = Field(
        max_length=const.EXAMPLE_MAX_LEN,
    )
    example_sentence_translation: str | None = Field(
        max_length=const.EXAMPLE_TRANSLATION_MAX_LEN, 
    )

    @field_validator("spelling")
    def to_lowercase(cls, v: str) -> str:
        return v.strip().lower()

# --- delete ---
class DeleteWordRequest(BaseModel): 
    user_word_id: str

