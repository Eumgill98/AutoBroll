from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
import uuid

from autobroll.nle.schema import Track

class Timeline(BaseModel):
    timeline_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    tracks: List[Track] = Field(default_factory=list)

    duration: Optional[float] = None

    fps: float = Field(default=30.0, gt=0)

    resolution: Tuple[int, int] = Field(default=(1920, 1080))

    creation_time: datetime = Field(default_factory=datetime.utcnow)

    metadata: Dict[str, object] = Field(default_factory=dict)

    @model_validator(mode="after")
    def compute_duration(self):
        if not self.tracks:
            self.duration = 0.0
            return self

        max_end = 0.0
        for track in self.tracks:
            for clip in track.clips:
                max_end = max(max_end, clip.timeline_end)

        self.duration = max_end
        return self