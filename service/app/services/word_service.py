import re
from typing import List, Tuple 
from pymongo.database import Database
from pymongo import errors as mongo_errors
from pydantic import ValidationError

from repositories.word_repository import WordRepository
from repositories.user_word_repository import UserWordRepository
import core.config as config
from models.word import Entry, Item 

from core.errors import ServiceError, BadRequestError, ConflictError

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY

class WordService:
    """Business logic for word operations including DeepSeek integration."""
    def __init__(self, db: Database):
        self.words = WordRepository(db)
        self.user_words = UserWordRepository(db)

    def get_word_entries_for_user(self, user_id: str) -> List[Entry]:
        """Return the word entries linked to the given user."""
        items = self.get_word_items_for_user(user_id)
        return [item.entry for item in items]

    def get_word_items_for_user(self, user_id: str) -> List[Item]: 
        """ Return the word items linked to the given user. """
        try: 
            word_ids = self.user_words.list_word_ids_by_user(user_id)
            if not word_ids: 
                return []
            return self.words.find_by_ids(word_ids)

        except ValidationError: 
            raise ServiceError("Corrupted word data in DB")
        except mongo_errors.PyMongoError:
            raise ServiceError("Database error while fetching words")

    # --- register --- 
    def register_word(self, entry: Entry, user_id: str) -> str: 
        """
            Entryが含まれていないならDBにNew Itemを加える
            Itemのregistered_countをインクリメント
            user_wordテーブルに加える
        """
        self._validate_entry(entry)

        try: 
            word_id = self.words.upsert_and_inc_entry(entry)
        except mongo_errors.PyMongoError as e:
            raise ServiceError("Failed to upsert word entry") from e

        try: 
            if self.user_words.exists_link(user_id, word_id): 
                raise ConflictError(f"Word '{entry.word}' is already registered by this user.")
        except mongo_errors.PyMongoError as e: 
            raise ServiceError("Failed to check user-word links") from e

        try: 
            return self.user_words.create_link(user_id, word_id)
        except mongo_errors.PyMongoError as e: 
            raise ServiceError("Failed to create user-word link") from e

    # --- search and suggestion ---
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

    def suggest_items(self, input_word: str, limit: int, cap: int = 100) -> List[Item]: 
        if not input_word:
            raise BadRequestError("input_word is required")

        try: 
            candidate_items = self.make_candidates_from_word(input_word, cap)
        except mongo_errors.PyMongoError as e: 
            raise ServiceError("Failed to make suggest candidates") from e

        if not candidate_items: 
            return [] 

        scored: List[Tuple[float, Item]] = []  # (score, Item)
        lw = input_word.lower()
        for it in candidate_items:
            w = it.entry.word
            if not w:
                continue
            score = self.lcs_score(lw, w.lower())
            scored.append((score, it))

        scored.sort(key=lambda t: (-t[0], -t[1].registered_count, len(t[1].entry.word), t[1].entry.word))

        return [pair[1] for pair in scored[:limit]]


    # --- internal validation ---
    def _validate_entry(self, entry: Entry) -> None:
        """Validate Entry payload for business rules."""
        if not entry or not (entry.word and entry.meaning):
            raise BadRequestError("Entry must contain 'word' and 'meaning'")
        # Keep lengths reasonable (example thresholds)
        if len(entry.word) > 64:
            raise BadRequestError("word is too long")
        if len(entry.meaning) > 2048:
            raise BadRequestError("meaning is too long")
