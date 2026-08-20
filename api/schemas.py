"""
schemas.py — Pydantic models that define exactly what shape each
route's JSON response takes. FastAPI uses these to validate outgoing
data AND auto-generate the Swagger docs — that's the main reason to
pick FastAPI over Flask: the docs and the validation come from the
same source of truth instead of being written twice.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LatestReading(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    grid_id: int
    zone_name: str
    location: str
    max_capacity: float
    temperature: float
    humidity: float
    load_percentage: float
    recorded_at: datetime


class CriticalZone(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    grid_id: int
    zone_name: str
    location: str
    load_percentage: float
    temperature: float
    recorded_at: datetime
    severity: str


class HistoryReading(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reading_id: int
    grid_id: int
    zone_name: str
    temperature: float
    humidity: float
    load_percentage: float
    recorded_at: datetime


class GridDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    grid_id: int
    zone_name: str
    location: str
    max_capacity: float
    created_at: datetime
    latest_load_percentage: float | None = None
    latest_temperature: float | None = None
    latest_recorded_at: datetime | None = None