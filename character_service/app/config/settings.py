from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_POSTGRES_HOST: str = "localhost"
    AUTH_POSTGRES_USER: str = "postgres"
    AUTH_POSTGRES_PASSWORD: str = "postgres"
    AUTH_POSTGRES_PORT: str = "35432"
    AUTH_POSTGRES_DB: str = "dnd_character"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.AUTH_POSTGRES_USER}:{self.AUTH_POSTGRES_PASSWORD}@{self.AUTH_POSTGRES_HOST}:{self.AUTH_POSTGRES_PORT}/{self.AUTH_POSTGRES_DB}"

    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
