from pydantic import BaseModel 
from typing import List

class WordBase(BaseModel): 
    word: str 
    meaning: str

class ExampleSentenceBase(BaseModel): 
    example_sentence: str | None = None
    example_sentence_translation: str | None = None

class WordEntryBase(WordBase, ExampleSentenceBase): 
    pass

class WordResponseBase(WordEntryBase):
    word_id: str 

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

