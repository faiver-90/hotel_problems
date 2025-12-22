from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class DatabaseSettings(BaseSettings):
    postgres_db: str = Field("orders", alias="POSTGRES_DB")
    postgres_user: str = Field("orders", alias="POSTGRES_USER")
    postgres_password: str = Field("", alias="POSTGRES_PASSWORD")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class Settings(BaseSettings):
    debug: bool = Field(False, alias="DEBUG")

    database: DatabaseSettings = DatabaseSettings()

    secret_key: str = Field("", alias="SECRET_KEY")

    allowed_hosts: str = Field(
        "localhost,127.0.0.1", alias="DJANGO_ALLOWED_HOSTS"
    )
    django_settings_module: str = Field(
        "core.settings.dev", alias="DJANGO_SETTINGS_MODULE"
    )

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        extra="ignore",
    )


settings = Settings()
