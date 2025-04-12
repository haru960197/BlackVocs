from pydantic import Field
from pydantic_settings import BaseSettings
import os


DB_NAME = os.getenv('DB_NAME') 
COLLECTION_NAME = os.getenv('COLLECTION_NAME') 
DB_URI = os.getenv('DB_URI')
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))

class DBConfig(BaseSettings):
    DB_USERNAME: str = Field(description="DBのユーザ名")
    DB_PASSWORD: str = Field(description="DBのパスワード")
    DB_HOST: str = Field(description="DBのホスト名")
    DB_PORT: str = Field(description="DBのポート番号")

db_config = DBConfig()