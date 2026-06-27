"""PostgreSQL settings for {{cookiecutter.service_name}}."""

from typing import ClassVar, Dict, Optional
from urllib.parse import quote_plus
from pydantic import Field, SecretStr, computed_field
from src.configs.base_settings import BaseSettings


class PostgresSettings(BaseSettings):
    PREFIX: ClassVar[str] = "POSTGRES"

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="postgres")
    password: SecretStr = Field(default=SecretStr("postgres"))
    db: str = Field(default="{{cookiecutter.service_name}}_db")
    min_pool_size: int = Field(default=5)
    max_pool_size: int = Field(default=20)
    pool_timeout: int = Field(default=30)
    pool_recycle: int = Field(default=1800)
    use_ssl: bool = Field(default=False)
    ssl_mode: Optional[str] = Field(default=None)
    connect_timeout: int = Field(default=10)
    command_timeout: int = Field(default=30)

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> str:
        pw = quote_plus(self.password.get_secret_value())
        return f"postgresql+asyncpg://{self.user}:{pw}@{self.host}:{self.port}/{self.db}"

    @computed_field
    @property
    def alembic_database_uri(self) -> str:
        pw = quote_plus(self.password.get_secret_value())
        uri = f"postgresql+psycopg2://{self.user}:{pw}@{self.host}:{self.port}/{self.db}"
        if self.use_ssl:
            uri += f"?sslmode={'require' if not self.ssl_mode else self.ssl_mode}"
        return uri

    @computed_field
    @property
    def sqlalchemy_engine_args(self) -> Dict:
        return {
            "pool_pre_ping": True,
            "pool_size": self.min_pool_size,
            "max_overflow": self.max_pool_size - self.min_pool_size,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "connect_args": {
                "timeout": self.connect_timeout,
                "command_timeout": self.command_timeout,
                "server_settings": {"application_name": "{{cookiecutter.service_name}}"},
            },
        }
