import re
from typing import List, Tuple 
from pymongo.database import Database
import unicodedata
import hashlib
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

    # --- get user word list --- 
    def get_word_items_by_user_id(self, user_id: str) -> List[Item]: 
        """ 
        Return the word items linked to the given user. 

        Args: 
            user_id (str): current user's user_id

        Returns: 
            items (List[Item]): user's word items
        """
        try: 
            word_ids = self.user_words.get_word_ids_by_user_id(user_id)
            return self.words.get_items_by_word_ids(word_ids)

        except ValidationError as e: 
            raise ServiceError(f"Data validation error: {e}")
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

    # --- suggest word ---
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
        return self.words.get_items_by_word_subseq(subseq, limit)

    def suggest_items(self, input_word: str, limit: int, cap: int = 100) -> List[Item]: 
        """
        get input_word and return suggest word items which are collected using the algorithm
        
        Args: 
            input_word(str) : input word which is written by user 
            limit(int) : maximum number of suggestion
            cap(int) : maximum number of word items which are collected when sorted by lcs

        Returns: 
            items(List[Item]) : suggest items 
        """
        try: 
            # 1) lcsの長さが大きいものから順番に取る（最大N個）
            candidate_items = self.make_candidates_from_word(input_word, cap)
            if not candidate_items: 
                return [] 
            
            # 2) (score, item)という形でsuggest itemsをlistにまとめる
            scored: List[Tuple[float, Item]] = []  
            lw = input_word.lower()
            for it in candidate_items:
                w = it.entry.word
                score = self.lcs_score(lw, w.lower())
                scored.append((score, it))

            # 2. itemをregistered_countが大きいものの順に並べる
            scored.sort(key=lambda t: (-t[0], -t[1].registered_count, len(t[1].entry.word), t[1].entry.word))

            return [pair[1] for pair in scored[:limit]]
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

    # --- register word --- 
    def register_word(self, entry: Entry, user_id: str) -> str: 
        """
        Entryが含まれていないならDBにNew Itemを加える
        Itemのregistered_countをインクリメント
        user_wordテーブルに加える

        Args: 
            entry(Entry) : entry to register 
            user_id(str) : current user's id

        Returns: 
            registered_id(str) : new user_word_id
            
        """

        self._validate_entry(entry)

        try: 
            fpr = self.entry2fingerprint(entry)

            # 1) get word_id, if None, create a new one
            word_id = self.words.get_id_by_fpr(fpr)
            if word_id is None: 
                word_id = self.words.create_item(fpr, entry)
            if not word_id: 
                raise ServiceError("Failed to get word_id")

            # 2) check if the user has alerady registered the word item
            if self.user_words.get_link(user_id, word_id):
                raise ConflictError("Word item is already registered by this user.")

            # 3) increment registered_count 
            self.words.increment_registered_count(word_id)

            # 4) create link and return 
            return self.user_words.create_link(user_id, word_id)
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

    # --- delete a word item from user_word collection ---
    def delete_user_item(self, word_id: str, user_id: str) -> str: 
        """
        delete a word item from user_word collection if the item exists in it

        Args: 
            word_id (str): word_id to delete from user collection 
            user_id (str): current user id 

        Returns: 
            user_word_id (str): deleted item id (no longer exist in the user_word collection
        """
        
        try: 
            # 1) check if the item is in the collection 
            if not self.words.exists_word_id(word_id): 
                raise BadRequestError("Word item does not exist in the dictionary")
            
            # 2. check if user_word link exists
            user_word_id = self.user_words.get_link(user_id, word_id)
            if not user_word_id: 
                raise BadRequestError("Word item have not been registered by the current user")

            # 3. declement register_word_count
            registered_count = self.words.get_registered_count_by_id(word_id)
            if registered_count <= 0: 
                raise BadRequestError("Registered count must be greater than 0")
            self.words.decrement_registered_count(word_id)

            # 4. delete the link
            result = self.user_words.delete_link(user_id, word_id)
            if not result:
                raise ServiceError("Failed to delete user_word item")

            return result 
        
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

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


    # --- fingerprint ---
    def _canon_text(self, s: str) -> str:
        """Return a canonicalized string for hashing.
        - Unicode NFKC normalization (unify width & symbols)
        - Trim leading/trailing whitespace
        - Collapse consecutive whitespace into a single space
        - Lowercase for ASCII letters (language-agnostic, safe for English words)
        """
        # Normalize Unicode (e.g., full-width -> half-width, compatibility forms)
        s = unicodedata.normalize("NFKC", s)
        # Strip leading/trailing whitespace
        s = s.strip()
        # Collapse all whitespace sequences to a single space
        s = re.sub(r"\s+", " ", s)
        # Lowercase (affects Latin letters; Japanese etc. remains unchanged)
        s = s.lower()
        return s

    def entry2fingerprint(self, entry: Entry) -> str:
        """Create a deterministic fingerprint for an Entry.
        Uses BLAKE2b-128 over a versioned, canonical payload.
        """
        parts = [
            self._canon_text(entry.word),
            self._canon_text(entry.meaning),
            self._canon_text(entry.example_sentence),
            self._canon_text(entry.example_sentence_translation),
        ]
        # Versioned payload to allow future changes without breaking old items
        payload = "entry:v1\n" + "\n".join(parts)

        # blake2b with 16-byte digest (128-bit) is short & collision-resistant for this use
        digest = hashlib.blake2b(payload.encode("utf-8"), digest_size=16).hexdigest()
        return digest

