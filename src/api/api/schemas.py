from uuid import UUID
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, field_validator
from typing_extensions import TypedDict

__all__ = [
    "SuccessResponse",
    "PingResponse",
    "SearchBody",
    "SearchResponse",
]


class TimeToFloatMixin:
    @field_validator("time_created", "time_updated", mode="before", check_fields=False)
    @classmethod
    def datetime_to_float(cls, v: datetime) -> float:
        return v.timestamp()


class SuccessResponse(BaseModel):
    success: bool = True


class PingResponse(BaseModel):
    response: str = "pong"


class DirectionOut(TimeToFloatMixin, BaseModel):
    direction_id: UUID
    university_id: int
    university_name: str
    faculty_id: int
    faculty_name: str
    cosine_distance: float


class SearchBody(BaseModel):
    city_title: str = Query(description="city_title", default="")
    about: str = Query(description="about", default="")
    activities: str = Query(description="activities", default="")
    books: str = Query(description="books", default="")
    games: str = Query(description="games", default="")
    interests: str = Query(description="interests", default="")
    threshold: float | None = Query(description="threshold", default=None)
    limit: int = Query(description="result length limit", default=15)


class SearchResponse(TypedDict):
    items: list[DirectionOut]
