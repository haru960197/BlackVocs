from dotenv import load_dotenv
load_dotenv()

import os

DB_NAME = os.getenv('DB_NAME') 
COLLECTION_NAME = os.getenv('COLLECTION_NAME') 
DB_URI = os.getenv('mongodb://localhost:27017/')
