from typing import TYPE_CHECKING
from pydantic import BaseModel, Field
from bson import ObjectId 

if TYPE_CHECKING:
    from schemas.word_schemas import Item as SchemaItem, ItemCreate as SchemaItemCreate

class Entry(BaseModel):
    word: str
    meaning: str
    example_sentence: str
    example_sentence_translation: str

    def to_schema_item(self) -> "SchemaItemCreate":
        from schemas.word_schemas import ItemCreate as SchemaItemCreate
        return SchemaItemCreate(
            word=self.word, 
            meaning=self.meaning, 
            example_sentence=self.example_sentence, 
            example_sentence_translation=self.example_sentence_translation,
        )

class Item(BaseModel):
    id: ObjectId = Field(alias = "_id", default=None)
    entry: Entry 
    fingerprint: str = Field(..., description = "deterministic fingerprint for enties")
    registered_count: int = Field(default = 0, ge = 0, description = "Number of users who registered this word")

    class Config:
        populate_by_name = True 
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    
    def to_schema_item(self) -> "SchemaItem":
        from schemas.word_schemas import Item as SchemaItem
        return SchemaItem(
            id=str(self.id),
            word=self.entry.word,
            meaning=self.entry.meaning,
            example_sentence=self.entry.example_sentence,
            example_sentence_translation=self.entry.example_sentence_translation,
        )
