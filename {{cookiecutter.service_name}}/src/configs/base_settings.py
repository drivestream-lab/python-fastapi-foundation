"""Base configuration settings for {{cookiecutter.service_name}}."""

from abc import ABC
from typing import Any, ClassVar, Dict, Type, TypeVar, cast

from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict

from src.logging import get_logger

logger = get_logger()
T = TypeVar("T", bound="BaseSettings")


class BaseSettings(PydanticBaseSettings, ABC):
    """Base class for all settings — singleton + env-prefix pattern."""

    PREFIX: ClassVar[str] = ""
    _instances: ClassVar[Dict[str, "BaseSettings"]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        prefix = getattr(cls, "PREFIX", "")
        if not prefix:
            raise ValueError(f"{cls.__name__} must define a non-empty PREFIX class variable")
        cls.model_config = SettingsConfigDict(
            env_prefix=f"{cls.PREFIX}_",
            env_file=".env",
            env_file_encoding="utf-8",
            env_nested_delimiter="__",
            case_sensitive=False,
            extra="ignore",
            validate_default=True,
        )

    @classmethod
    def get_instance(cls: Type[T]) -> T:
        class_name = cls.__name__
        if class_name not in cls._instances:
            cls._instances[class_name] = cls()
        return cast(T, cls._instances[class_name])
