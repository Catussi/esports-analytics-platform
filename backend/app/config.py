from functools import lru_cache
import ssl
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "eSports Analytics Platform"
    app_env: str = "development"
    debug: bool = True

    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "esports_user"
    mysql_password: str = "changeme"
    mysql_database: str = "esports_analytics"
    mysql_ssl: bool = False
    mysql_ssl_ca: str = ""

    sqlalchemy_echo: bool = False
    sqlalchemy_pool_size: int = 5
    sqlalchemy_max_overflow: int = 10

    ml_model_path: str = "app/ml/models/kmeans_pca_model.joblib"
    cors_origins: str = "http://localhost:4200,http://127.0.0.1:4200"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def mysql_connect_args(self) -> dict:
        if not self.mysql_ssl:
            return {}

        ca_path = self.mysql_ssl_ca.strip()
        if ca_path and Path(ca_path).is_file():
            ssl_context = ssl.create_default_context(cafile=ca_path)
        else:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        return {"ssl": ssl_context}


@lru_cache
def get_settings() -> Settings:
    return Settings()
