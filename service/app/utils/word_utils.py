from pymongo.database import Database
import requests
from schemas.word_schemas import (
    Item as ItemSchema,
)
from models.word_models import Item as ItemModel
import core.config as config

WORD_COLLECTION_NAME = config.WORD_COLLECTION_NAME
DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY

def model_to_schema(item: ItemModel) -> ItemSchema:
    return ItemSchema(
        word=item.word,
        meaning=item.meaning,
        example_sentence=item.example_sentence,
        example_sentence_translation=item.example_sentence_translation
    )

def generate_and_insert_item(word: str, db: Database) -> ItemModel:
    """
    単語を受け取り、APIで例文などを含むItemを生成、データベースへ保存
    """

    word_collection = db[WORD_COLLECTION_NAME]
    item = word2item_with_API(word)
    word_collection.insert_one(item.model_dump())

    return item

def word2item_with_API(word: str) -> ItemModel:
    """
    Generate a word item using DeepSeek API based on the given English word
    not put it into the dictionary
    only generating the item

    Args:
        word (str): An English word to look up.

    Returns:
        ItemModel: A data model including the word, its meaning, an English example sentence,
                   and the Japanese translation of the example.
    """

    prompt = f"""
    単語: {word}

    1. この英単語の意味を日本語で簡潔に説明してください。
    2. この単語を使った自然な英文を1文作ってください。
    3. その英文の日本語訳を教えてください。

    出力形式:
    意味: ...
    英文: ...
    和訳: ...
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",  
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7 # appropriate for our program, I think
    }

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")

    content = response.json()["choices"][0]["message"]["content"]

    meaning = example_sentence = example_sentence_translation = ""
    for line in content.splitlines():
        if line.startswith("意味:"):
            meaning = line.replace("意味:", "").strip()
        elif line.startswith("英文:"):
            example_sentence = line.replace("英文:", "").strip()
        elif line.startswith("和訳:"):
            example_sentence_translation = line.replace("和訳:", "").strip()

    if not (meaning and example_sentence and example_sentence_translation):
        raise ValueError("Failed to parse DeepSeek response correctly")

    return ItemModel(
        word=word,
        meaning=meaning,
        example_sentence=example_sentence,
        example_sentence_translation=example_sentence_translation
    )