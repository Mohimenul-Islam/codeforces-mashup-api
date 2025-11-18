from sqlmodel import SQLModel, Field, JSON, Column
from typing import Optional, List
from pydantic import field_validator


class MashupRequest(SQLModel):
    username: str
    num_problems: int = 5
    min_rating: int = 1400
    max_rating: int = 1600

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        if len(v) > 24:
            raise ValueError('Username too long')
        return v.strip()

    @field_validator('num_problems')
    @classmethod
    def validate_num_problems(cls, v):
        if v < 1:
            raise ValueError('Number of problems must be at least 1')
        if v > 100:
            raise ValueError('Number of problems cannot exceed 100')
        return v

    @field_validator('min_rating')
    @classmethod
    def validate_min_rating(cls, v):
        if v < 800:
            raise ValueError('Minimum rating cannot be less than 800')
        if v > 3500:
            raise ValueError('Minimum rating cannot exceed 3500')
        return v

    @field_validator('max_rating')
    @classmethod
    def validate_max_rating(cls, v):
        if v < 800:
            raise ValueError('Maximum rating cannot be less than 800')
        if v > 3500:
            raise ValueError('Maximum rating cannot exceed 3500')
        return v


class Problem(SQLModel):
    name: str
    contest_id: int
    index: str
    rating: int


class Mashup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_data: str
    problems: str = Field(sa_column=Column(JSON))


class MashupResponse(SQLModel):
    mashup_id: int
    problems: List[Problem]