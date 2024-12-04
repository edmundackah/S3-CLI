from typing import Optional
from pydantic import BaseModel, HttpUrl

class ChangeRecordException(Exception):
    """Custom exception for handling unexpected API responses."""
    pass


class AssignmentGroup(BaseModel):
    """Shared model for assignment group"""
    link: HttpUrl
    value: str


class ChangeRecordResponse(BaseModel):
    """Model for a valid response (status code 200)"""
    valid: bool
    number: str
    short_description: str
    assignment_group: AssignmentGroup
    description: str
    state: str
    start_date: Optional[str] = None  # Optional for Incident responses
    end_date: Optional[str] = None   # Optional for Incident responses
    invalid_reason: str


class NotFoundResponse(BaseModel):
    """Model for a 404 error response"""
    status: int
    error: str
    description: str