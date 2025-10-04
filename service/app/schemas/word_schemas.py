from pydantic import BaseModel, StringConstraints
from typing import List, Annotated

WordText = Annotated[str, StringConstraints(min_length=1, max_length=45, strip_whitespace=True)]
SentenceText = Annotated[str, StringConstraints(max_length=120, strip_whitespace=True)]

class WordBase(BaseModel): 
    word: WordText
    meaning: WordText

class ExampleSentenceBase(BaseModel): 
    example_sentence: SentenceText | None = None
    example_sentence_translation: SentenceText | None = None

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

