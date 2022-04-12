from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str
    api_secret: str
    database_url: str
    debug: bool = False
    protocol: str = "http"
    host: str = "0.0.0.0"
    port: int = "8000"
    pagination_limit: int = 50
    access_token_expiration_secs: int = 120
    refresh_token_expiration_secs: int = 600

    class Config:
        env_file = ".env"

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"


settings = Settings()
