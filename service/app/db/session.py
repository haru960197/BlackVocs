# from urllib import parse

# from config import db_config
# from pymongo import MongoClient
# from pymongo.database import Database

# USER_NAME = parse.quote_plus(db_config.DB_USERNAME)
# PASSWORD = parse.quote_plus(db_config.DB_PASSWORD)
# HOST = db_config.DB_HOST
# PORT = db_config.DB_PORT

# MONGO_DATABASE_URL: str = f"mongodb://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}"

# client = MongoClient(MONGO_DATABASE_URL)


# def get_db() -> Database:
#     """DB取得

#     Returns:
#         Database: データべース
#     """
#     db: Database = client.db
#     return db