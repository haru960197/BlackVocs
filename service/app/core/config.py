import os
from dotenv import load_dotenv

load_dotenv()

## user DB
USER_COLLECTION_NAME = os.getenv("USER_COLLECTION_NAME", "")
WORD_COLLECTION_NAME = os.getenv("WORD_COLLECTION_NAME", "")
USER_WORD_COLLECTION_NAME=os.getenv("USER_WORD_COLLECTION_NAME", "")

#jwt
JWT_KEY = os.getenv("JWT_KEY")

# API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# Service port 
SERVICE_PORT = os.getenv("SERVICE_PORT", "8000")

MONGO_DB_URL = os.getenv("MONGO_DB_URL", "")
