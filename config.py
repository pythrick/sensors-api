from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str
    database_url: str
    debug: bool = False
    pagination_limit: int = 50

    class Config:
        env_file = ".env"


settings = Settings()
