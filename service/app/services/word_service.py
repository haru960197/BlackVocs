import re
from typing import List, Tuple 
from pymongo.database import Database
from pymongo import errors as mongo_errors
from pydantic import ValidationError
from models.common import ExampleBaseModel, GetUserWordModel, PyObjectId, WordBaseModel, WordEntryModel
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
            user_word_models = self.user_words.find_models_by_user_id(user_id)
            result: List[GetUserWordModel] = []
            for uw_model in user_word_models: 
                word_model = self.words.find_model_by_word_id(uw_model.word_id)
                if word_model is None: 
                    raise ServiceError("Failed to word_model")
                tmp = GetUserWordModel(
                    word_id=uw_model.word_id, 
                    word_base=word_model.word_base, 
                    example_base=uw_model.example_base
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
        return self.words.search_models_by_word_subseq(subseq, limit)

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
            # 1) lcsの長さが大きいものから順番に取る（最大N個）
            candidate_models = self.collect_candidates_by_word_str(input_word, cap)
            if not candidate_models: 
                return [] 
            
            # 2) (score, model)という形でsuggest modelsをlistにまとめる
            scored: List[Tuple[float, WordModel]] = []  
            lw = input_word.lower()
            for im in candidate_models:
                w = im.word_base.word
                score = self.lcs_score(lw, w.lower())
                scored.append((score, im))

            # 3) itemをregistered_countが大きいものの順に並べる
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
            # 1) get word_id, if None, create a new one
            word_model = self.words.find_model_by_word_base_model(entry_model.word_base)
            if word_model: 
                word_entry_id = word_model.id
            else: 
                word_entry_id = self.words.create(WordModel(word_base=entry_model.word_base))

            if not word_entry_id: 
                raise ServiceError("Failed to get word_id")

            # 2) check if the user has alerady registered the word item
            if self.user_words.find_link(user_id, word_entry_id):
                raise ConflictError("Word item is already registered by this user.")

            # 3) increment registered_count 
            self.words.increment_registered_count(word_entry_id)

            # 4) create link and return 
            new_entry_model = UserWordModel(
                user_id=user_id, 
                word_id=word_entry_id, 
                example_base=entry_model.example_base,
            )
            return self.user_words.create(new_entry_model)
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
            # 1) check if the item is in the collection 
            if not self.words.find_model_by_word_id(word_id): 
                raise BadRequestError("Word item does not exist in the dictionary")
            
            # 2. check if user_word link exists
            user_word_id = self.user_words.find_link(user_id, word_id)
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

