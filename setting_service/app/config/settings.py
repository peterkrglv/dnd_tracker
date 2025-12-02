from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SETTING_MONGO_HOST: str = "setting_db"
    SETTING_MONGO_USER: str
    SETTING_MONGO_PASSWORD: str
    SETTING_MONGO_PORT: int = 27017
    SETTING_MONGO_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"mongodb://{self.SETTING_MONGO_USER}:{self.SETTING_MONGO_PASSWORD}@{self.SETTING_MONGO_HOST}:{self.SETTING_MONGO_PORT}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3

    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS", "CORS_METHODS", "CORS_HEADERS", mode="before")
    def _parse_list_fields(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            try:
                import json

                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
