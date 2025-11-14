import re
from typing import List, Tuple 
from pymongo.database import Database
from pymongo import errors as mongo_errors
from pydantic import ValidationError
from core import const
from models.user_word import UsageExample, UserWordModel
from models.word import WordDetails, WordModel 
from repositories.word_repository import WordRepository
from repositories.user_word_repository import UserWordRepository
from core.oid import PyObjectId
import core.config as config
from core.errors import ServiceError, BadRequestError, ConflictError
from schemas.word_schemas import DeleteWordRequest, GetWordContentRequest, GetWordListResponse, GetWordListResponseBase, GetWordContentResponse, RegisterWordRequest, SuggestWordsRequest, SuggestWordsResponse, SuggestWordsResponseBase

DEEPSEEK_API_KEY = config.DEEPSEEK_API_KEY
MAX_NUM_WORD_SUGGEST = const.MAX_NUM_WORD_SUGGEST
MAX_NUM_WORD_SUGGEST_CANDIDATE = const.MAX_NUM_WORD_SUGGEST_CANDIDATE


class WordService:
    """Business logic for word operations including DeepSeek integration."""
    def __init__(self, db: Database):
        self.words = WordRepository(db)
        self.user_words = UserWordRepository(db)

    # --- get user word list --- 
    def get_word_list_by_user_id(self, user_id: PyObjectId) -> GetWordListResponse: 
        """ 
        Return the word items linked to the given user. 
        """
        try: 
            user_word_models = self.user_words.find_all(user_id=user_id)

            word_list: list[GetWordListResponseBase] = []

            for m in user_word_models: 
                word = self.words.find(word_id=m.word_id)
                if word is None: 
                    raise ServiceError("Failed to word_model")

                item = GetWordListResponseBase(
                    user_word_id=str(m.id),
                    spelling=word.details.spelling, 
                    meaning=word.details.meaning, 
                )
                word_list.append(item)
            return GetWordListResponse(word_list=word_list) 

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

    # --- get word content --- 
    def get_word_content(self, payload: GetWordContentRequest) -> GetWordContentResponse: 
        try: 
            # find user_word model
            user_word_model = self.user_words.find(user_word_id=PyObjectId(payload.user_word_id))
            if user_word_model is None: 
                raise ServiceError("failed to find user_word_model")

            # get word model
            word_model = self.words.find(word_id=user_word_model.word_id)
            if word_model is None: 
                raise ServiceError("failed to find word_model")
           
            # create response 
            return GetWordContentResponse(
                user_word_id=str(user_word_model.id), 
                spelling=word_model.details.spelling, 
                meaning=word_model.details.meaning, 
                example_sentence=user_word_model.usage_example.sentence, 
                example_sentence_translation=user_word_model.usage_example.translation, 
            )

        except ValidationError as e: 
            raise ServiceError(f"Data validation error: {e}")
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

    # --- suggest word ---
    def generate_word_suggestion(self, payload: SuggestWordsRequest) -> SuggestWordsResponse: 
        """
        get input_word and return suggest word items which are collected using the algorithm
        """
        try: 
            # lcsの長さが大きいものから順番に取る（最大N個）
            words = self.__collect_candidates_by_word_str(input_str=payload.input_str)

            # (score, item)という形でsuggest itemsをlistにまとめる
            scored: List[Tuple[float, WordModel]] = []  
            lw = payload.input_str.lower()
            for m in words:
                w = m.details.spelling
                score = self.__lcs_score(lw, w.lower())
                scored.append((score, m))

            # itemをregistered_countが大きいものの順に並べる
            scored.sort(key=lambda t: (-t[0], -t[1].registration_count, len(t[1].details.spelling), t[1].details.spelling))

            word_list: List[SuggestWordsResponseBase] = []
            for m in scored[:MAX_NUM_WORD_SUGGEST]:
                if not m[1].id: 
                    raise ServiceError("failed to get id in WordModel item")

                item = SuggestWordsResponseBase(
                    word_id=str(m[1].id), 
                    spelling=m[1].details.spelling, 
                    meaning=m[1].details.meaning,
                )
                word_list.append(item)

            return SuggestWordsResponse(word_list=word_list)
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

    # --- register word --- 
    def register_word(self, payload: RegisterWordRequest, user_id: PyObjectId) -> None: 
        """
        Entryが含まれていないならDBにNew Itemを加える
        Itemのregistered_countをインクリメント
        user_wordテーブルに加える
        """

        try: 
            entry_word_details = WordDetails(spelling=payload.spelling, meaning=payload.meaning)
            entry_model = self.words.find(word_details=entry_word_details)
            if entry_model is None: 
                new_word_model = WordModel(details=entry_word_details)
                word_id = self.words.create(new_word_model)
            else:
                word_id = entry_model.id
            if not word_id: 
                raise ServiceError("Failed to get word_id")

            # check if the user has alerady registered the word item
            if self.user_words.find(user_id=user_id, word_id=word_id):
                raise ConflictError("Word item is already registered by this user.")

            # increment registered_count 
            self.words.increment_registration_count(word_id)

            # create link and return 
            new_user_word_model = UserWordModel(
                user_id=user_id, 
                word_id=word_id, 
                usage_example=UsageExample(sentence=payload.example_sentence, translation=payload.example_sentence_translation),
            )

            self.user_words.create(new_user_word_model)
            return            

        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

    # --- delete a word item from user_word collection ---
    def delete_word(self, payload: DeleteWordRequest) -> None: 
        """
        delete a word item from user_word collection if the item exists in it
        """
        
        try: 
            # check if user_word link exists
            user_word_model = self.user_words.find(user_word_id=PyObjectId(payload.user_word_id))
            if not user_word_model: 
                raise BadRequestError("Word item have not been registered by the current user")

            # declement register_word_count
            word_model = self.words.find(word_id=user_word_model.word_id)
            if word_model is None: 
                raise ServiceError("Failed to find word model to delete")

            if word_model.registration_count <= 0: 
                raise ServiceError("Registered count must be greater than 0")
            self.words.decrement_registration_count(PyObjectId(user_word_model.word_id))

            # delete the link
            if not user_word_model.id: 
                raise ServiceError("user_word id is empty")
            deleted_user_word_model = self.user_words.delete(user_word_id=user_word_model.id)

            if not deleted_user_word_model:
                raise ServiceError("Failed to delete user word item")
            return         
        except mongo_errors.PyMongoError as e:
            raise ServiceError(f"Database error: {e}")
        except Exception as e:
            raise ServiceError(f"service error: {e}")

    # --- private ---
    def __lcs_len(self, a: str, b: str) -> int:
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

    def __lcs_score(self, query: str, candidate: str) -> float:
        """Normalize LCS length by max length to get [0,1]."""
        if not query or not candidate:
            return 0.0
        return self.__lcs_len(query, candidate) / max(len(query), len(candidate))

    def __make_subsequence_regex(self, q: str) -> str:
        """Build a regex like 'a.*b.*c' to quickly prefilter subsequence-like matches."""
        parts = [re.escape(ch) for ch in q]
        return ".*".join(parts)

    def __collect_candidates_by_word_str(self, input_str: str, limit: int = MAX_NUM_WORD_SUGGEST_CANDIDATE) -> List[WordModel]:
        """
        Build a subsequence regex from input_word and fetch candidate words from DB.
        """
        subseq = self.__make_subsequence_regex(input_str)
        return self.words.find_by_word_subseq(subseq, limit)

