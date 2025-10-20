from pydantic import BaseModel
from core.oid import PyObjectId
from models.word import WordBaseModel, ExampleBaseModel
from schemas.word_schemas import GetUserWordResponseBase

# --- common models ---
class GetUserWordModel(BaseModel): 
    user_word_id: PyObjectId 
    word_base: WordBaseModel
    example_base: ExampleBaseModel

    def to_schema(self) -> "GetUserWordResponseBase": 
        from schemas.word_schemas import GetUserWordResponseBase
        return GetUserWordResponseBase(
            user_word_id=str(self.user_word_id), 
            word=self.word_base.word,
            meaning=self.word_base.meaning, 
            example_sentence=self.example_base.example_sentence, 
            example_sentence_translation=self.example_base.example_sentence_translation,
        )

class AIGenerateModel(BaseModel): 
    word_base: WordBaseModel
    example_base: ExampleBaseModel
