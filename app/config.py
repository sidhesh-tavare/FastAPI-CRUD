from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from pathlib import Path
from pydantic import Field

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
# print(settings.model_dump())
# print(ENV_PATH)
# print(f"\n{Path(__file__).resolve()}")

class LoginService(BaseSettings):
    # Map .env variables to single-underscore internal attributes
    signature: str = Field(alias="SIGNATURE", exclude=True)
    algorithm: str = Field(alias="ALGORITHM", exclude=True)

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_ignore_empty=True,
        extra="ignore",
    )

    @property
    def get_signature(self) -> str:
        return self.signature
loginsettings = LoginService()
# print(loginsettings.get_signature)
    
        
    