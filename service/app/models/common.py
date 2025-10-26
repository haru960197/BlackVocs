from pydantic import BaseModel
from core.oid import PyObjectId
from models.word import WordBaseModel, ExampleBaseModel

# --- common models ---
class GetUserWordModel(BaseModel): 
    word_id: PyObjectId 
    word_base: WordBaseModel
    example_base: ExampleBaseModel

    def to_schema(self) -> "GetUserWordListResponseBase": 
        from schemas.word_schemas import GetUserWordListResponseBase
        return GetUserWordListResponseBase(
            word_id=str(self.word_id), 
            word=self.word_base.word,
            meaning=self.word_base.meaning, 
            example_sentence=self.example_base.example_sentence, 
            example_sentence_translation=self.example_base.example_sentence_translation,
        )

class AIGenerateModel(BaseModel): 
    word_base: WordBaseModel
    example_base: ExampleBaseModel
