from bson import ObjectId
from typing import Any
from pydantic_core import core_schema
from pydantic import GetJsonSchemaHandler, BaseModel
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string"}

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# --- components for DB models ---
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
    exmpale_sentence_translation: str

# --- common models ---
class GetUserWordModel(BaseModel): 
    id: PyObjectId 
    word_base: WordBaseModel
    example_base: ExampleBaseModel

    def to_schema(self) -> "WordResponseBase": 
        from schemas.word_schemas import WordResponseBase
        return WordResponseBase(
            word_id=self.id, 
            word=self.word_base.word,
            meaning=self.word_base.meaning, 
            example_sentence=self.example_base.example_sentence, 
            example_sentence_translation=self.example_base.exmpale_sentence_translation,
        )


