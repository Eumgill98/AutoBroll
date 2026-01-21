from typing import Dict
from pydantic import BaseModel, Field, model_validator
import uuid

class Clip(BaseModel):
    clip_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    source_video_path: str

    # source time(original media)
    in_time: float = Field(..., ge=0)
    out_time: float = Field(..., gt=0)

    # timeline time
    timeline_start: float = Field(..., ge=0)
    timeline_end: float = Field(..., gt=0)

    speed: float = Field(default=1.0, gt=0)

    metadata: Dict[str, object] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_times(self):
        if self.out_time <= self.in_time:
            raise ValueError("out_time must be greater than in_time")

        if self.timeline_end <= self.timeline_start:
            raise ValueError("timeline_end must be greater than timeline_start")

        return self
    
    @property
    def duration(self) -> float:
        return (self.out_time - self.in_time) / self.speed