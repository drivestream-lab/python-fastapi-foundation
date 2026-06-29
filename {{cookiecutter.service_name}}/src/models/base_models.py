"""Base Pydantic models for {{cookiecutter.service_name}}."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TimestampedModel(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
