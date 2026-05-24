from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Quality MES"
    DATABASE_URL: str = "sqlite:///./quality_mes.db"
    SECRET_KEY: str = "change-this-to-a-random-secret-key-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
