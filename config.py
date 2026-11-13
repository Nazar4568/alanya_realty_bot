# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    gemini_api_key: str
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/alanya_realty"
    n8n_webhook_url: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()