import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the DQ Guardian application.
    Settings are loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
        description="The database URL for the DQ Guardian application.",
    )
    DQ_SAVE_PATH: str = Field(
        default="./data_quality_results",
        description="The path to save the data quality results.",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get the settings for the DQ Guardian application.
    The settings are cached to avoid loading them multiple times.
    """
    return Settings()