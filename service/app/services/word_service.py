from typing import List, Tuple
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

    def _generate_item_via_AI(self, word: str) -> dict[str, str] | None:
        self.ai.generate_entry(word)
    
    def get_word_entries_for_user(self, user_id: str) -> List[Entry]:
        """Return the word entries linked to the given user."""
        word_ids = self.user_words.list_word_ids_by_user(user_id)
        if not word_ids:
            return []
        items: List[Item] = self.words.find_by_ids(word_ids)
        entries = [item.entry for item in items]
        return entries
    
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
        
