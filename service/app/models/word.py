from pydantic import BaseModel, ConfigDict, conint, Field
from core.oid import PyObjectId
from core.errors import ServiceError

class WordBaseModel(BaseModel): 
    word: str
    meaning: str | None

class WordBaseModelWithId(WordBaseModel):
    id: PyObjectId

    def to_schema(self) -> "SuggestWordsResponseBase": 
        from schemas.word_schemas import SuggestWordsResponseBase 
        return SuggestWordsResponseBase(
            word_id=str(self.id), 
            word=self.word, 
            meaning=self.meaning,
        )

class ExampleBaseModel(BaseModel): 
    example_sentence: str | None = None
    example_sentence_translation: str | None = None

class WordEntryModel(BaseModel):
    word_base: WordBaseModel
    example_base: ExampleBaseModel

    def to_schema(self) -> "GenerateNewWordEntryResponse": 
        from schemas.word_schemas import GenerateNewWordEntryResponse

        if not (self.word_base.meaning and self.example_base.example_sentence and self.example_base.example_sentence_translation): 
            raise ServiceError("meaning or example_sentence or example_sentence_translation is None")

        return GenerateNewWordEntryResponse(
            word=self.word_base.word, 
            meaning=self.word_base.meaning, 
            example_sentence=self.example_base.example_sentence, 
            example_sentence_translation=self.example_base.example_sentence_translation, 
        )

class WordModel(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    word_base: WordBaseModel
    registered_count: conint(ge=0) = Field(default=0)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PyObjectId: str},
    )

