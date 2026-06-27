"""Redis settings for {{cookiecutter.service_name}}."""

from typing import Any, ClassVar, Dict, Optional
from pydantic import Field, SecretStr, computed_field
from src.configs.base_settings import BaseSettings


class RedisSettings(BaseSettings):
    PREFIX: ClassVar[str] = "REDIS"

    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    password: Optional[SecretStr] = Field(default=None)
    db: int = Field(default=0)
    prefix: str = Field(default="ds_{{cookiecutter.service_name}}:")
    use_ssl: bool = Field(default=False)
    socket_timeout: int = Field(default=5)
    connection_timeout: int = Field(default=5)
    retry_on_timeout: bool = Field(default=True)
    pool_max_size: int = Field(default=10)
    default_ttl: int = Field(default=3600)

    @computed_field
    @property
    def connection_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "host": self.host, "port": self.port, "db": self.db,
            "socket_timeout": self.socket_timeout,
            "socket_connect_timeout": self.connection_timeout,
            "retry_on_timeout": self.retry_on_timeout,
            "max_connections": self.pool_max_size,
        }
        if self.password:
            params["password"] = self.password.get_secret_value()
        if self.use_ssl:
            params["ssl"] = True
        return params
