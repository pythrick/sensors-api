from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str
    database_url: str
    debug: bool = False
    pagination_limit: int = 50
    port: int = 8000
    host: str = "0.0.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
