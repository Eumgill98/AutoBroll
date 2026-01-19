from abc import ABC, abstractmethod

from autobroll.asr.schema import AudioData

class BaseASR(ABC):
    """
    A abstract class for ASR model.
    """
    @abstractmethod
    def transcribe(
        self,
        audio: AudioData,
    ):
        ...