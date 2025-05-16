from pydantic import BaseModel

class Item(BaseModel):
    id: str
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str
