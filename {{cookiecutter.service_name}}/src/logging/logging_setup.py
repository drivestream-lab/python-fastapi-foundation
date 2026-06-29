"""Logging setup for {{cookiecutter.service_name}}."""

import atexit
import json as _json
import logging
import os
import sys
import threading
import traceback
import uuid
from datetime import UTC, datetime
from typing import Any, Callable, Optional
from loguru import logger
from src.logging.logging_context import get_correlation_id

_SERVICE_NAME = "{{cookiecutter.service_name}}"
is_logging_shutdown = False
_logging_lock = threading.RLock()
_is_logging_setup = False

TEXT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {message}"
)
FILE_TEXT_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
)


def _flat_json_line(record: Any, service: str, environment: str) -> str:
    out: dict[str, Any] = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "service": service,
        "environment": environment,
        "logger": record["name"],
        "function": record["function"],
        "line": record["line"],
    }
    for k, v in record["extra"].items():
        if k not in out:
            out[k] = v
    exc = record["exception"]
    if exc:
        out["exception_type"] = exc.type.__name__
        out["exception_message"] = str(exc.value)
        out["stack_trace"] = "".join(traceback.format_exception(exc.type, exc.value, exc.traceback))
    return _json.dumps(out, default=str) + "\n"


def _make_flat_json_sink(service: str, environment: str, writer: Callable[[str], None]):
    def sink(message: Any) -> None:
        writer(_flat_json_line(message.record, service, environment))

    return sink


def _context_patcher(record: Any) -> None:
    cid = get_correlation_id()
    if cid:
        record["extra"]["correlation_id"] = cid


class ResilientSink:
    def __init__(self, sink: Any) -> None:
        self.sink = sink
        self.errors = 0

    def write(self, message: str) -> None:
        global is_logging_shutdown
        if is_logging_shutdown:
            return
        try:
            self.sink.write(message)
        except (ValueError, IOError):
            self.errors += 1
            if self.errors >= 10:
                is_logging_shutdown = True


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno  # type: ignore
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def shutdown_logging() -> None:
    global is_logging_shutdown
    with _logging_lock:
        if is_logging_shutdown:
            return
        is_logging_shutdown = True
    logger.remove()


def setup_logging(settings: Optional[Any] = None) -> None:
    global _is_logging_setup
    with _logging_lock:
        if _is_logging_setup:
            return
        atexit.register(shutdown_logging)
        logger.remove()

        log_level = getattr(settings, "log_level", "INFO") if settings else "INFO"
        log_format = getattr(settings, "log_format", "text") if settings else "text"
        is_dev = getattr(settings, "is_development", True) if settings else True
        log_dir = getattr(settings, "log_dir", "logs") if settings else "logs"
        environment = str(getattr(getattr(settings, "environment", None), "value", "development"))

        os.makedirs(log_dir, exist_ok=True)
        use_json = log_format.lower() == "json"
        date_str = datetime.now(UTC).strftime("%Y%m%d")
        log_file = os.path.join(log_dir, f"{_SERVICE_NAME}_{date_str}.log")

        if use_json:

            def _append_json_line(line: str) -> None:
                with open(log_file, "a", encoding="utf-8") as log_f:
                    log_f.write(line)

            logger.add(
                _make_flat_json_sink(_SERVICE_NAME, environment, _append_json_line),
                level=log_level,
                enqueue=True,
            )
            logger.add(
                _make_flat_json_sink(_SERVICE_NAME, environment, ResilientSink(sys.stdout).write),
                level=log_level,
                enqueue=True,
            )
        else:
            logger.add(
                log_file,
                rotation="00:00",
                retention="30 days",
                compression="gz",
                level=log_level,
                format=FILE_TEXT_FORMAT,
                enqueue=True,
            )
            logger.add(
                ResilientSink(sys.stdout).write,
                level=log_level,
                format=TEXT_FORMAT,
                backtrace=True,
                diagnose=is_dev,
                enqueue=True,
                colorize=is_dev,
            )

        logger.configure(
            patcher=_context_patcher,
            extra={
                "service": _SERVICE_NAME,
                "environment": environment,
                "correlation_id": str(uuid.uuid4()),
            },
        )
        root = logging.getLogger()
        root.handlers = []
        root.addHandler(InterceptHandler())
        root.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        logging.getLogger("watchfiles").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        _is_logging_setup = True


def get_logger() -> Any:
    return logger
