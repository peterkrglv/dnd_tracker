from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    USER_POSTGRES_HOST: str
    USER_POSTGRES_USER: str
    USER_POSTGRES_PASSWORD: str
    USER_POSTGRES_PORT: str
    USER_POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.USER_POSTGRES_USER}:{self.USER_POSTGRES_PASSWORD}@{self.USER_POSTGRES_HOST}:{self.USER_POSTGRES_PORT}/{self.USER_POSTGRES_DB}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3

    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
