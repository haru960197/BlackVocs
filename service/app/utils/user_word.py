from pymongo.database import Database
from bson import ObjectId
import core.config as config
import models.user_word as user_word_model

USER_WORD_COLLECTION_NAME = config.USER_WORD_COLLECTION_NAME

def insert_user_word(user_id: str, word_id: str, db: Database) -> str:
    """
    Insert a user-word relation into the user_word collection 

    Args:
        user_id (str): ID of the user
        word_id (str): ID of the word
        db (Database): MongoDB database instance

    Returns:
        str: The ID of the inserted user_word document
    """

    user_word = user_word_model.UserWordModel(
        user_id=user_id,
        word_id=word_id
    )

    insert_dict = user_word.dict()
    insert_dict["user_id"] = ObjectId(insert_dict["user_id"])
    insert_dict["word_id"] = ObjectId(insert_dict["word_id"])

    result = db[USER_WORD_COLLECTION_NAME].insert_one(insert_dict)

    return str(result.inserted_id)


def get_user_word_ids(user_id: str, db: Database) -> list[str]:
    collection = db[USER_WORD_COLLECTION_NAME]
    cursor = collection.find({"user_id": ObjectId(user_id)})
    return [str(doc["word_id"]) for doc in cursor]
