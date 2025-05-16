from pymongo.database import Database
from schemas.vocab_schemas import (
    Item as ItemSchema,
)
from models.vocab_models import Item as ItemModel
import core.config as config
import uuid

VOCAB_COLLECTION_NAME = config.VOCAB_COLLECTION_NAME

def model_to_schema(item: ItemModel) -> ItemSchema:
    if not item.id:
        raise ValueError("item.id is missing")
    return ItemSchema(
        id=item.id,
        word=item.word,
        meaning=item.meaning,
        example_sentence=item.example_sentence,
        example_sentence_translation=item.example_sentence_translation
    )

def generate_and_insert_item(word: str, db: Database) -> ItemModel:
    vocab_collection = db[VOCAB_COLLECTION_NAME]

    meaning = f"Meaning of {word}"
    example_sentence = f"This is an example sentence using the word {word}."
    example_sentence_translation = f"{word} を使った例文です。"

    item = ItemModel(
        id=str(uuid.uuid4()),
        word=word,
        meaning=meaning,
        example_sentence=example_sentence,
        example_sentence_translation=example_sentence_translation,
    )

    vocab_collection.insert_one(item.model_dump())

    return item