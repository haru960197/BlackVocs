from typing import List, Tuple
from pymongo.database import Database
from bson import ObjectId
import requests
from repositories.word_repository import WordRepository
from repositories.user_word_repository import UserWordRepository
import core.config as config

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY

class WordService:
    """Business logic for word operations including DeepSeek integration."""
    def __init__(self, db: Database):
        self.words = WordRepository(db)
        self.user_words = UserWordRepository(db)

    # ---------- DeepSeek ----------
    def _generate_item_via_deepseek(self, word: str) -> dict:
        """Call DeepSeek and parse outputs into {word, meaning, example_sentence, example_sentence_translation}."""
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
            "Content-Type": "application/json",
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"DeepSeek API error: {resp.status_code} - {resp.text}")

        content = resp.json()["choices"][0]["message"]["content"]
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

        return {
            "word": word,
            "meaning": meaning,
            "example_sentence": example_sentence,
            "example_sentence_translation": example_sentence_translation,
        }

    # ---------- Use cases for your schema ----------

    def add_new_word(self, word: str, user_id_str: str) -> Tuple[dict, str]:
        """
        Generate (via DeepSeek) and insert a word if needed, then link to user.
        Returns: (word_doc, user_word_id)
        """
        # 1) Upsert-like: reuse existing exact spelling if present (case-insensitive)
        existing = self.words.find_by_word_exact(word, case_insensitive=True)
        if existing:
            word_doc = existing
            word_oid = existing["_id"]
        else:
            gen = self._generate_item_via_deepseek(word)
            word_id = self.words.create(gen)
            word_oid = ObjectId(word_id)
            word_doc = {**gen, "_id": word_oid}

        # 2) Link (user, word)
        user_oid = ObjectId(user_id_str)
        if self.user_words.exists_link(user_oid, word_oid):
            # Already linked -> return a stable id-like string (or re-query)
            link_id = ""  # or fetch existing link _id if you prefer
        else:
            link_id = self.user_words.create_link(user_oid, word_oid)

        return word_doc, link_id

    def get_user_word_list(self, user_id_str: str) -> List[dict]:
        """Return word documents linked to the given user."""
        user_oid = ObjectId(user_id_str)
        word_ids = self.user_words.list_word_ids_by_user(user_oid)
        if not word_ids:
            return []
        return self.words.find_by_ids([str(wid) for wid in word_ids])

    def suggest_words(self, q: str, limit: int = 10) -> List[dict]:
        """Exact-first then prefix-fill search."""
        q = (q or "").strip()
        if not q:
            return []

        exact = self.words.find_by_word_exact(q, case_insensitive=True)
        results: List[dict] = []
        exclude_ids: List[ObjectId] = []
        if exact:
            results.append(exact)
            exclude_ids.append(exact["_id"])

        remain = max(0, limit - len(results))
        if remain > 0:
            results += self.words.find_prefix(q=q, limit=remain, case_insensitive=True, exclude_ids=exclude_ids or None)
        return results
