import re
import requests
import core.config as config
from models.word import ExampleBaseModel, WordBaseModel, WordEntryModel

from requests import RequestException
from core.errors import ServiceError

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY
DEEPSEEK_URL = config.DEEPSEEK_URL or ""

LABEL_RX = {
    "meaning": re.compile(r"^\s*意味\s*[:：\-]?\s*(.*)\s*$"),
    "en": re.compile(r"^\s*英文\s*[:：\-]?\s*(.*)\s*$"),
    "ja": re.compile(r"^\s*和訳\s*[:：\-]?\s*(.*)\s*$"),
}

class GenerativeAIService: 
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        key = (api_key or DEEPSEEK_API_KEY or "").strip()
        url = (DEEPSEEK_URL or "").strip()
        if not key:
            raise RuntimeError("DeepSeek API key is missing")
        if not url:
            raise RuntimeError("DeepSeek API URL is missing")

        self.api_key = key
        self.url = url
        self.timeout = timeout

    def generate_entry(self, word: str) -> WordEntryModel:
        """
        Return dict(word, meaning, example_sentence, example_sentence_translation).

        Args: 
            word(str) : word which current user writes     
        
        Returns: 
            WordEntryModel : generated entry
        """

        prompt = (
            f"単語: {word}\n\n"
            "1. この英単語の意味を日本語で簡潔に説明してください。\n"
            "2. この単語を使った自然な英文を1文作ってください。\n"
            "3. その英文の日本語訳を教えてください。\n\n"
            "出力形式:\n"
            "意味: ...\n"
            "英文: ...\n"
            "和訳: ...\n"
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }

        try: 
            # post prompt
            resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                raise ServiceError(f"DeepSeek API error: {resp.status_code} {resp.text[:200]}")

            # get contents
            choices = resp.json().get("choices") or []
            content = ""
            if choices: 
                msg = choices[0].get("message") or {}
                content = (msg.get("content") or "").strip()
            if not content:
                raise ServiceError("DeepSeek returned empty content")

            # extract each components
            meaning = example_sentence = example_sentence_translation = ""
            for raw_line in content.splitlines():
                s = raw_line.strip()
                if not s:
                    continue
                m = LABEL_RX["meaning"].match(s)
                if m:
                    meaning = m.group(1).strip()
                    continue
                m = LABEL_RX["en"].match(s)
                if m:
                    example_sentence = m.group(1).strip()
                    continue
                m = LABEL_RX["ja"].match(s)
                if m:
                    example_sentence_translation = m.group(1).strip()
                    continue
            if not (meaning and example_sentence and example_sentence_translation):
                raise ServiceError("DS response missing required fields")

            return WordEntryModel(
                word_base=WordBaseModel(word=word, meaning=meaning), 
                example_base=ExampleBaseModel(example_sentence=example_sentence, example_sentence_translation=example_sentence_translation), 
            )
        except RequestException as e: 
            raise ServiceError("Failed to call DeepSeek API") from e
        except Exception as e:
            raise ServiceError("Failed to parse DeepSeek JSON response") from e


