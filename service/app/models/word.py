from pydantic import BaseModel, ConfigDict, conint, Field
from models.common import WordBaseModel, PyObjectId

class WordBaseModel(BaseModel): 
    word: str
    meaning: str

    def to_schema(self) -> "WordBase": 
        from schemas.word_schemas import WordBase
        return WordBase(
            word=self.word, 
            meaning=self.meaning,
        )

class ExampleBaseModel(BaseModel): 
    example_sentence: str
    example_sentence_translation: str

class WordEntryModel(BaseModel):
    word_base: WordBaseModel
    example_base: ExampleBaseModel

    def to_schema(self) -> "WordEntryBase": 
        from schemas.word_schemas import WordEntryBase
        return WordEntryBase(
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

