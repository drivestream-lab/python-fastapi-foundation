"""Application exceptions for {{cookiecutter.service_name}}."""

from typing import Any, Dict, Optional


class BaseAppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 500,
                 details: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(BaseAppException):
    def __init__(self, resource_type: str, resource_id: Any,
                 message: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        msg = message or f"{resource_type} with ID {resource_id} not found"
        d = details or {}
        d.update({"resource_type": resource_type, "resource_id": str(resource_id)})
        super().__init__(code="RESOURCE_NOT_FOUND", message=msg, status_code=404, details=d)


class ValidationError(BaseAppException):
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None,
                 details: Optional[Dict[str, Any]] = None):
        d = details or {}
        if field_errors:
            d["field_errors"] = field_errors
        super().__init__(code="VALIDATION_ERROR", message=message, status_code=400, details=d)


class ServiceUnavailableError(BaseAppException):
    def __init__(self, service_name: str, message: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        d = details or {}
        d["service_name"] = service_name
        super().__init__(
            code="SERVICE_UNAVAILABLE",
            message=message or f"Service {service_name} is unavailable",
            status_code=503, details=d,
        )
