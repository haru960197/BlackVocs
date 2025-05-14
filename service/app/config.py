from pydantic import Field
from pydantic_settings import BaseSettings
import os

# DBの情報をクラスでまとめる
class DBConfig(BaseSettings):
    DB_USERNAME: str = Field(description="DBのユーザ名")
    DB_PASSWORD: str = Field(description="DBのパスワード")
    DB_HOST: str = Field(description="DBのホスト名")
    DB_PORT: str = Field(description="DBのポート番号")

db_config = DBConfig()

DB_NAME = os.getenv('DB_NAME') 
COLLECTION_NAME = os.getenv('COLLECTION_NAME') 
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
DB_URI = f"mongodb://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@mongo:27017/"

JWT_KEY = os.getenv('JWT_KEY')
