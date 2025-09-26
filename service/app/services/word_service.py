import re
from typing import List, Tuple 
from pymongo.database import Database
from pymongo import errors as mongo_errors
from pydantic import ValidationError
from models.common import GetUserWordModel, PyObjectId, WordBaseModel, WordEntryModel
from models.user_word import UserWordModel
from models.word import WordModel
from repositories.word_repository import WordRepository
from repositories.user_word_repository import UserWordRepository
import core.config as config
from core.errors import ServiceError, BadRequestError, ConflictError

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY

class WordService:
    """Business logic for word operations including DeepSeek integration."""
    def __init__(self, db: Database):
        self.words = WordRepository(db)
        self.user_words = UserWordRepository(db)

    # --- get user word list --- 
    def get_user_word_list_by_user_id(self, user_id: PyObjectId) -> List[GetUserWordModel]: 
        """ 
        Return the word items linked to the given user. 

        Args: 
            user_id (PyObjectId): current user's user_id

        Returns: 
            items (List[GetUserWordModel]): user's word items
        """
        try: 
            user_word_models = self.user_words.find_user_word(user_id=user_id)
            if user_word_models is None: 
                return []

            result: List[GetUserWordModel] = []
            for m in user_word_models: 
                word = self.words.find_word(word_id=m.word_id)
                if word is None: 
                    raise ServiceError("Failed to word_model")
                tmp = GetUserWordModel(
                    word_id=m.word_id, 
                    word_base=word.word_base, 
                    example_base=m.example_base
                )
                result.append(tmp)

            return result

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

    def collect_candidates_by_word_str(self, input_word: str, limit: int) -> List[WordModel]:
        """
        Build a subsequence regex from input_word and fetch candidate words from DB.
        """
        subseq = self.make_subsequence_regex(input_word)
        return self.words.find_models_by_word_subseq(subseq, limit)

    def collect_suggest_models(self, input_word: str, limit: int, cap: int = 100) -> List[WordBaseModel]: 
        """
        get input_word and return suggest word items which are collected using the algorithm
        
        Args: 
            input_word(str) : input word which is written by user 
            limit(int) : maximum number of suggestion
            cap(int) : maximum number of word items which are collected when sorted by lcs

        Returns: 
            items(List[WordBaseModel]) : suggest items 
        """
        try: 
            # lcsの長さが大きいものから順番に取る（最大N個）
            candidate_models = self.collect_candidates_by_word_str(input_word, cap)
            if not candidate_models: 
                return [] 
            
            # (score, item)という形でsuggest itemsをlistにまとめる
            scored: List[Tuple[float, WordModel]] = []  
            lw = input_word.lower()
            for m in candidate_models:
                w = m.word_base.word
                score = self.lcs_score(lw, w.lower())
                scored.append((score, m))

            # itemをregistered_countが大きいものの順に並べる
            scored.sort(key=lambda t: (-t[0], -t[1].registered_count, len(t[1].word_base.word), t[1].word_base.word))

            return [pair[1].word_base for pair in scored[:limit]]
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

    # --- register word --- 
    def register_word(self, entry_model: WordEntryModel, user_id: PyObjectId) -> PyObjectId: 
        """
        Entryが含まれていないならDBにNew Itemを加える
        Itemのregistered_countをインクリメント
        user_wordテーブルに加える

        Args: 
            entry_model(WordBaseModel) : entry to register 
            user_id(PyObjectId) : current user's id

        Returns: 
            registered_id(PyObjectId) : new user_word_id
            
        """

        try: 
            word = self.words.find_word(word_base=entry_model.word_base)
            if word is None: 
                new_word = WordModel(word_base=entry_model.word_base)
                word_id = self.words.create(new_word)
            else:
                word_id = word.id
            if not word_id: 
                raise ServiceError("Failed to get word_id")

            # check if the user has alerady registered the word item
            if self.user_words.find_user_word(user_id=user_id, word_id=word_id):
                raise ConflictError("Word item is already registered by this user.")

            # increment registered_count 
            self.words.increment_registered_count(word_id)

            # create link and return 
            new_user_word_model = UserWordModel(
                user_id=user_id, 
                word_id=word_id, 
                example_base=entry_model.example_base,
            )
            return self.user_words.create(new_user_word_model)
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

    # --- delete a word item from user_word collection ---
    def delete_user_item(self, word_id: PyObjectId, user_id: PyObjectId) -> PyObjectId: 
        """
        delete a word item from user_word collection if the item exists in it

        Args: 
            word_id (PyObjectId): word_id to delete from user collection 
            user_id (PyObjectId): current user id 

        Returns: 
            user_word_id (PyObjectId): deleted item id (no longer exist in the user_word collection
        """
        
        try: 
            # check if the item is in the collection 
            word = self.words.find_word(word_id=word_id)
            if not word: 
                raise ServiceError("Word item does not exist in the dictionary")
            
            # check if user_word link exists
            user_word = self.user_words.find_user_word(user_id, word_id)
            if not user_word: 
                raise BadRequestError("Word item have not been registered by the current user")

            # declement register_word_count
            if word.registered_count <= 0: 
                raise ServiceError("Registered count must be greater than 0")
            self.words.decrement_registered_count(word_id)

            # delete the link
            deleted_user_word = self.user_words.delete(user_word_id=user_word.id)
            if not deleted_user_word:
                raise ServiceError("Failed to delete user word item")
            
            return deleted_user_word.id
        
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")

