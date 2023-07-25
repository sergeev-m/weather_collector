import os

from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BasePath = Path(__file__).resolve().parent.parent.parent

Versions = os.path.join(BasePath, 'migrations', 'versions')

LogPath = os.path.join(BasePath, 'log')

CsvPath = os.path.join(BasePath, 'data')


class Settings(BaseSettings):

    # FastAPI
    TITLE: str = 'FastAPI'
    DESCRIPTION: str = 'weather collector'
    DEBUG: bool = bool(os.environ.get("DEBUG"))
    VERSION: str = "0.1"

    # Env Token
    API_KEY: str = os.environ.get("API_KEY")

    # Log
    LOG_FILENAME: str = 'weather_error.log'

    # Weather
    WEATHER_URL: str = 'https://api.openweathermap.org/data/2.5/weather'
    CITY_CSV_FILENAME: str = 'cities.csv'
    CELERY_TASK_NAME: str = 'weather_collector'
    NUMBER_OF_RESULT_CITIES: int = 50
    TEMP_UPDATE_INTERVAL: int = 60 * 60  # second

    # Env Postgres
    USER: str = os.environ.get("POSTGRES_USER", "postgres")
    PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
    PORT: str = os.environ.get("POSTGRES_PORT", "5432")
    DB_NAME: str = os.environ.get("POSTGRES_DB", "junov_net")
    DB_ECHO: bool = False
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')

    # Redis
    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: str = os.environ.get('REDIS_PORT')

    @property
    def database_url(self) -> Optional[PostgresDsn]:
        return f"postgresql://{self.USER}:{self.PASSWORD}" \
               f"@{self.HOST}:{self.PORT}/{self.DB_NAME}"

    @property
    def redis_url(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
