from typing import List, Dict, Any
import re
from pymongo.database import Database
from bson import ObjectId #type: ignore
from repositories.word_repository import WordRepository
from repositories.user_word_repository import UserWordRepository
import core.config as config
from utils.generative_AI_client import GenerativeAIClient
from models.word import Entry, Item 

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY

class WordService:
    """Business logic for word operations including DeepSeek integration."""
    def __init__(self, db: Database, ai_client: GenerativeAIClient | None = None):
        self.words = WordRepository(db)
        self.user_words = UserWordRepository(db)
        self.ai = ai_client or GenerativeAIClient()

    def get_word_entries_for_user(self, user_id: str) -> List[Entry]:
        """Return the word entries linked to the given user."""
        items = self.get_word_items_for_user(user_id)
        entries = [item.entry for item in items]
        return entries

    def get_word_items_for_user(self, user_id: str) -> List[Item]: 
        """ Return the word items linked to the given user. """
        word_ids = self.user_words.list_word_ids_by_user(user_id)
        if not word_ids: 
            return []
        items: List[Item] = self.words.find_by_ids(word_ids)
        return items

    # --- register --- 
    def register_word(self, entry: Entry, user_id: str) -> str: 
        """
            Entryが含まれていないならDBにNew Itemを加える
            Itemのregistered_countをインクリメント
            user_wordテーブルに加える
        """
        word_id = self.words.find_by_entry(entry)

        if word_id: 
            if self.user_words.exists_link(user_id, word_id):
                raise ValueError(f"Word '{entry.word}' is already registered by this user.")
            else:
                word_id = self.words.upsert_and_inc_entry(entry)
        else:
            word_id = self.words.upsert_and_inc_entry(entry)

        return self.user_words.create_link(user_id, word_id)

    # --- search ---
    def lcs_len(self, a: str, b: str) -> int:
        """Return LCS length using O(len(a)*len(b)) DP."""
        n, m = len(a), len(b)
        # Small optimization: keep a rolling 1D DP array
        prev = [0] * (m + 1)
        for i in range(1, n + 1):
            cur = [0]
            ai = a[i - 1]
            for j in range(1, m + 1):
                if ai == b[j - 1]:
                    cur.append(prev[j - 1] + 1)
                else:
                    cur.append(max(prev[j], cur[-1]))
            prev = cur
        return prev[-1]

    def lcs_score(self, query: str, candidate: str) -> float:
        """Normalize LCS length by max length to get [0,1]."""
        if not query or not candidate:
            return 0.0
        return self.lcs_len(query, candidate) / max(len(query), len(candidate))

    def make_subsequence_regex(self, q: str) -> str:
        """Build a regex like 'a.*b.*c' to quickly prefilter subsequence-like matches."""
        parts = [re.escape(ch) for ch in q]
        return ".*".join(parts)

    def make_candidates_from_word(self, input_word: str, limit: int) -> List[Item]:
        """
        Build a subsequence regex from input_word and fetch candidate words from DB.
        """
        subseq = self.make_subsequence_regex(input_word)
        return self.words.find_candidates_by_entry_word_subsequence(subseq, limit)

