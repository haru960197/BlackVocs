from pydantic import BaseModel 
from typing import List

from models.common import PyObjectId

class WordBase(BaseModel): 
    word: str 
    meaning: str

class ExampleSentenceBase(BaseModel): 
    example_sentence: str | None
    example_sentence_translation: str | None

class WordResponseBase(WordBase, ExampleSentenceBase):
    word_id: PyObjectId

# --- get user word list ---
class GetUserWordListResponse(BaseModel):
    word_items: List[WordResponseBase]

# --- suggest ---
class SuggestWordsRequest(BaseModel): 
    input_word: str
    max_num: int = 10 

class SuggestWordsResponse(BaseModel):
    word_items: List[WordBase]

# --- generate ---
class GenerateNewWordEntryRequest(BaseModel): 
    word: str

class GenerateNewWordEntryResponse(WordBase, ExampleSentenceBase): 
    pass

# --- register word ---
class RegisterWordRequest(WordBase, ExampleSentenceBase): 
    pass

class RegisterWordResponse(BaseModel):  
    user_word_id: PyObjectId 

# --- delete ---
class DeleteWordRequest(BaseModel): 
    word_id: PyObjectId

