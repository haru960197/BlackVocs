import re
from openai import OpenAI
from pymongo import MongoClient
import config
import models
from typing import List, Dict

# DeepSeek APIクライアント設定
client = OpenAI(
    api_key=config.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def connect_to_mongodb(uri=config.DB_URI):
    client = MongoClient(uri)
    return client[config.DB_NAME][config.COLLECTION_NAME]  


def add_new_word(item: models.Item) -> str:
    collection = connect_to_mongodb()
    result = collection.insert_one(item.to_dict())
    print(f"[Insert] ID: {result.inserted_id}")

    return str(result.inserted_id)


def get_all_items() -> List[models.Item]:
    """ DBに保存されている全ての単語情報を返す
    """
    collection = connect_to_mongodb()
    items = list(collection.find({}))
    return [doc_to_model(item) for item in items]


def generate_and_insert_item(word: str) -> models.Item:
    """ 単語を受け取って、意味・例文・和訳を取得 → MongoDBに保存する関数 
    """
    messages = [
        {
            "role": "user",
            "content": f"""Please provide the following about the English word "{word}" in the format below:

1. 意味（日本語で簡潔に）
2. 例文（小学生でも理解できる自然な英語文）
3. 和訳（例文の日本語訳）

Format:
1. 意味: ...
2. 例文: ...
3. 和訳: ...
"""
        }
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )

    full_text = response.choices[0].message.content.strip()

    # 正規表現で抽出
    meaning_match = re.search(r"1\. 意味:\s*(.*)", full_text)
    example_match = re.search(r"2\. 例文:\s*(.*)", full_text)
    translation_match = re.search(r"3\. 和訳:\s*(.*)", full_text)

    meaning = meaning_match.group(1).strip() if meaning_match else "Not found"
    example_sentence = example_match.group(1).strip() if example_match else "Not found"
    example_translation = translation_match.group(1).strip() if translation_match else "Not found"

    # Itemを作成
    item = models.Item(
        word=word,
        meaning=meaning,
        example_sentence=example_sentence,
        example_sentence_translation=example_translation
    )

    # MongoDBに保存
    item_id = add_new_word(item)

    return models.Item(
        id=item_id,
        word=word,
        meaning=meaning,
        example_sentence=example_sentence,
        example_sentence_translation=example_translation
    )


def doc_to_model(doc: Dict) -> models.Item:
    """ DBに保存されているdoc(document)をmodelに変換する
    """
    return models.Item(
        id=str(doc["_id"]),  # ObjectId → str に変換
        word=doc["word"],
        meaning=doc["meaning"],
        example_sentence=doc["exampleSentence"],
        example_sentence_translation=doc["exampleSentenceTranslation"]
    )
