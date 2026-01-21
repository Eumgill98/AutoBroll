from typing import Dict, Literal, List
from pydantic import BaseModel, Field
import uuid

from autobroll.nle.schema import Clip

class Track(BaseModel):
    track_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    track_type: Literal["video", "audio", "text"]

    clips: List[Clip] = Field(default_factory=list)

    position: int = Field(..., ge=0)

    properties: Dict[str, object] = Field(default_factory=dict)

    def sorted_clips(self) -> List[Clip]:
        return sorted(self.clips, key=lambda c: c.timeline_start)