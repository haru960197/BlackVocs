from pydantic import BaseModel, PostgresDsn

class Settings(BaseModel):
    SQLALCHEMY_DATABASE_URI: PostgresDsn = "postgresql://postgres:postgres@db:5432/test" # PostgreSQLを利用した場合の例
    SECRET_KEY: str = "..." # 省略
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()