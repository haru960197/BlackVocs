from pydantic import BaseModel, field_validator
from typing import List

class WordBase(BaseModel): 
    word: str 
    meaning: str | None = None

    @field_validator("word")
    def to_lowercase(cls, v: str) -> str:
        return v.strip().lower()

class ExampleSentenceBase(BaseModel): 
    example_sentence: str | None = None 
    example_sentence_translation: str | None = None

class WordEntryBase(WordBase, ExampleSentenceBase): 
    pass

class WordResponseBase(WordEntryBase):
    word_id: str 

# --- get user word list ---
class GetUserWordListResponse(BaseModel):
    word_list: List[WordResponseBase]

# --- suggest ---
class SuggestWordsRequest(BaseModel): 
    input_word: str
    max_num: int = 10 

class WordBaseWithId(WordBase): 
    word_id: str

class SuggestWordsResponse(BaseModel):
    word_list: List[WordBaseWithId]

# --- generate ---
class GenerateNewWordEntryRequest(WordEntryBase): 
    pass

class GenerateNewWordEntryResponse(WordEntryBase): 
    pass

# --- register word ---
class RegisterWordRequest(WordEntryBase): 
    pass

class RegisterWordResponse(BaseModel):  
    user_word_id: str

# --- delete ---
class DeleteWordRequest(BaseModel): 
    word_id: str

