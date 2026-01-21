from pydantic import BaseModel, Field
from typing import List, Optional

from autobroll.asr.schema import ASRSegment

class ASRResult(BaseModel):
    language: Optional[str] = Field(default=None)
    segments: List[ASRSegment] = Field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(seg.text for seg in self.segments)