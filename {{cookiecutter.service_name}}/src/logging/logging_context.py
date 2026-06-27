"""Logging context for {{cookiecutter.service_name}}."""

import contextvars, functools, uuid
from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional, TypeVar, Union
from uuid import UUID
from loguru import logger

correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="")
LogContextValue = Union[str, UUID, int, None]
F = TypeVar("F", bound=Callable[..., Any])


def get_correlation_id() -> str:
    return correlation_id_var.get()


def set_correlation_id(cid: str) -> None:
    correlation_id_var.set(cid)


def correlation_id(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        current = get_correlation_id()
        if not current:
            token = correlation_id_var.set(str(uuid.uuid4()))
            try:
                return func(*args, **kwargs)
            finally:
                correlation_id_var.reset(token)
        return func(*args, **kwargs)
    return wrapper  # type: ignore


class LoggingContext:
    def __init__(self, cid: Optional[str] = None):
        self.correlation_id = cid or str(uuid.uuid4())
        self.token = None

    def __enter__(self):
        self.token = correlation_id_var.set(self.correlation_id)
        return self

    def __exit__(self, *_):
        if self.token is not None:
            correlation_id_var.reset(self.token)


@contextmanager
def request_log_context(**fields: LogContextValue) -> Iterator[None]:
    """Bind domain IDs into loguru extra for nested logs."""
    bound = {k: str(v) for k, v in fields.items() if v is not None}
    if not bound:
        yield
        return
    with logger.contextualize(**bound):
        yield
