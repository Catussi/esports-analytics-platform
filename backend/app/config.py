from functools import lru_cache

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


@lru_cache
def get_settings() -> Settings:
    return Settings()
