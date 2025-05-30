from pymongo.database import Database
from bson import ObjectId

import core.config as config

USER_WORD_COLLECTION_NAME = config.USER_WORD_COLLECTION_NAME

def insert_user_word(user_id: str, word_id: str, db: Database) -> str:
    """
    Insert a user-word relation into the user_word collection.

    Args:
        user_id (str): ID of the user
        word_id (str): ID of the word
        db (Database): MongoDB database instance

    Returns:
        str: The ID of the inserted user_word document
    """
    result = db[USER_WORD_COLLECTION_NAME].insert_one({
        "user_id": ObjectId(user_id),
        "word_id": ObjectId(word_id),
    })
    return str(result.inserted_id)
