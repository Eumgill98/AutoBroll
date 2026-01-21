from pydantic import BaseModel, Field
from typing import Optional

class ASRWord(BaseModel):
    text: str = Field(...)
    start: float = Field(...)
    end: float = Field(...)
    confidence: Optional[float] = Field(default=None)
