import requests
import core.config as config
from models.word import Entry

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY
DEEPSEEK_URL = config.DEEPSEEK_URL

class GenerativeAIClient: 
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.timeout = timeout

    def generate_entry(self, word: str) -> Entry:
        """Return dict(word, meaning, example_sentence, example_sentence_translation)."""
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
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=self.timeout)
        if resp.status_code != 200:
            raise RuntimeError(f"DeepSeek API error: {resp.status_code} - {resp.text}")

        content = resp.json()["choices"][0]["message"]["content"]
        # --- parse
        meaning = example_sentence = example_sentence_translation = ""
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("意味:"):
                meaning = s.replace("意味:", "").strip()
            elif s.startswith("英文:"):
                example_sentence = s.replace("英文:", "").strip()
            elif s.startswith("和訳:"):
                example_sentence_translation = s.replace("和訳:", "").strip()

        if not (meaning and example_sentence and example_sentence_translation):
            raise ValueError("Failed to parse DeepSeek response correctly")

        return Entry(
            word=word,
            meaning=meaning,
            example_sentence=example_sentence,
            example_sentence_translation=example_sentence_translation,
        )
