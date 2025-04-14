from typing import Optional

class Item:
    def __init__(
        self,
        word: str,
        meaning: str,
        example_sentence: str,
        example_sentence_translation: str,
        id: Optional[str] = None, # 登録前はNone、登録後にセットされる
    ):
        self.id = id
        self.word = word
        self.meaning = meaning
        self.example_sentence = example_sentence
        self.example_sentence_translation = example_sentence_translation

    def to_dict(self, include_id: bool = False) -> dict:
        # NOTE: MongoDB用にキャメルケースに変換する
        data = {
            "word": self.word,
            "meaning": self.meaning,
            "exampleSentence": self.example_sentence,
            "exampleSentenceTranslation": self.example_sentence_translation
        }
        if include_id and self.id is not None:
            data["_id"] = self.id  # MongoDB用に _id をキーに使う場合
        return data
