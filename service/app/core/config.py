from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

# DB
class DBConfig(BaseSettings):
    DB_USERNAME: str = Field(description="DBのユーザ名")
    DB_PASSWORD: str = Field(description="DBのパスワード")
    DB_HOST: str = Field(description="DBのホスト名")
    DB_PORT: str = Field(description="DBのポート番号")

db_config = DBConfig()

## user DB
USER_COLLECTION_NAME = os.getenv("USER_COLLECTION_NAME")

#jwt
JWT_KEY = os.getenv("JWT_KEY")

# API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")