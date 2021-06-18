from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    access_token_url = "https://api.intra.42.fr/oauth/token"
    authorize_url = "https://api.intra.42.fr/oauth/authorize"
    api_base_url = "https://api.intra.42.fr/v2/"
    session_secret_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
