from pydantic import BaseModel, Field
from typing import List, Optional

from autobroll.asr.schema import ASRWord

class ASRSegment(BaseModel):
    text: str = Field(...)
    start: float = Field(...)
    end: float = Field(...)
    words: Optional[List[ASRWord]] = Field(default=None)