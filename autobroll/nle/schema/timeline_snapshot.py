from pydantic import BaseModel, Field
from datetime import datetime

from autobroll.nle.schema import Timeline

class TimelineSnapshot(BaseModel):
    timeline: Timeline

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    version: int = Field(..., ge=0)
