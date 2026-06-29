"""Qualified types for DI (protocol aliases) in {{cookiecutter.service_name}}."""

from typing import Protocol, AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresSessionFactory(Protocol):
    def __call__(self) -> AsyncContextManager[AsyncSession]: ...
