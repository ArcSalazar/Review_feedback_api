from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    APP_NAME: str = "Review Feedback API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
