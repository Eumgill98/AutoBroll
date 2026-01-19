from abc import ABC, abstractmethod
from typing import Optional, Any
from pydantic import BaseModel, Field

from autobroll.asr.schema import AudioData

class BaseASR(BaseModel, ABC):
    """
    A abstract class for ASR model.

    Fields:
        model: ASR model instance
    """
    model: Optional[Any] = Field(default=None, description="ASR model instance.")

    @abstractmethod
    def transcribe(
        self,
        audio: AudioData,
    ):
        ...