from pydantic import Field
from pydantic_settings import BaseSettings
import os


DB_NAME = os.getenv('DB_NAME') 
COLLECTION_NAME = os.getenv('COLLECTION_NAME') 
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
DB_URI = f"mongodb://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@mongo:27017/"
