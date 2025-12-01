from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CHARACTER_POSTGRES_HOST: str = "localhost"
    CHARACTER_POSTGRES_USER: str
    CHARACTER_POSTGRES_PASSWORD: str
    CHARACTER_POSTGRES_PORT: str = "45433"
    CHARACTER_POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.CHARACTER_POSTGRES_USER}:{self.CHARACTER_POSTGRES_PASSWORD}@{self.CHARACTER_POSTGRES_HOST}:{self.CHARACTER_POSTGRES_PORT}/{self.CHARACTER_POSTGRES_DB}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
