from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

class DatabaseSettings(BaseSettings):
    POSTGRES_USER : str 
    POSTGRES_PASSWORD : str 
    POSTGRES_SERVER : str 
    POSTGRES_PORT : int 
    POSTGRES_DB : str 

    @property
    def POSTGRES_URL(self)->str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_ignore_empty=True,
        extra='ignore')

settings = DatabaseSettings()
print(settings.model_dump())
# print(ENV_PATH)
# print(f"\n{Path(__file__).resolve()}")