"""Health response models for {{cookiecutter.service_name}}."""

from enum import Enum
from pydantic import BaseModel, Field


class HealthLivenessType(str, Enum):
    OK = "ok"


class HealthStatusType(str, Enum):
    UP = "up"
    DOWN = "down"


class HealthSimpleResponse(BaseModel):
    status: HealthLivenessType = Field(default=HealthLivenessType.OK)


class ServiceHealthDetailModel(BaseModel):
    status: HealthStatusType
    details: dict[str, bool] = Field(default_factory=dict)


class HealthDetailedResponse(BaseModel):
    status: HealthStatusType
    services: dict[str, ServiceHealthDetailModel] = Field(default_factory=dict)
