from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return str(v) # Always return string representation

class ExperimentMetrics(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    use_case: str
    context_level: str
    iteration: int
    prompt: str
    url: Optional[str] = None
    selectors: Optional[List[str]] = None
    metadata: Optional[dict] = None
    success: bool
    total_duration_ms: float  # in milliseconds
    api_time_ms: float
    quality: Optional[int] = None  # 1-5 scale
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
