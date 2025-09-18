from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/qa_db"
    app_name: str = "Q&A API Service"
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()