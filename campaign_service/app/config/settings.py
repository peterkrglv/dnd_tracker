from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CAMPAIGN_POSTGRES_HOST: str = "campaign_db"
    CAMPAIGN_POSTGRES_USER: str
    CAMPAIGN_POSTGRES_PASSWORD: str
    CAMPAIGN_POSTGRES_PORT: str = "5432"
    CAMPAIGN_POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.CAMPAIGN_POSTGRES_USER}:{self.CAMPAIGN_POSTGRES_PASSWORD}@{self.CAMPAIGN_POSTGRES_HOST}:{self.CAMPAIGN_POSTGRES_PORT}/{self.CAMPAIGN_POSTGRES_DB}"

    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
