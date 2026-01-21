from typing import Optional
import whisper

from autobroll.asr.base import BaseASR
from autobroll.asr.schema import AudioData, ASRResult, ASRSegment

class WhisperASR(BaseASR):
    """
    OpenAI Whisper-based ASR class.
    """
    def __init__(
        self,
        model_name: str = "large-v2",
        device: str = "cpu",
        language: Optional[str] = None,
    ):
        """
        Initialize the Whisper ASR engine.

        Args:
            model_name (str): Whisper model identifier
            device (str): Execution device ("cpu", "cuda")
            language (Optional[str]): Target language code (None for auto-detection)
        """
        self.model_name = model_name
        self.device = device
        self.language = language

        self.model = whisper.load_model(
            self.model_name,
            device=self.device,
        )

    def transcribe(
        self, 
        audio: AudioData,
    ) -> ASRResult:
        """
        Transcribe audio using Whisper.

        Args:
            audio (AudioData): Input audio data.

        Returns:
            ASRResult:
                - language: detected or specified language
                - segments: (segment-level timestamps only)
        """
        # load data
        if audio.path is not None:
            audio_input = str(audio.path)
        elif audio.waveform is not None:
            audio_input = audio.waveform
        else:
            raise ValueError("Invalid AudioData!")
        
        result = self.model.transcribe(
            audio_input,
            language=self.language,
        )

        segments = [
            ASRSegment(
                text=seg["text"].strip(),
                start=seg["start"],
                end=seg["end"],
                words=None, 
            )
            for seg in result.get("segments", [])
        ]

        return ASRResult(
            language=result.get("language"),
            segments=segments,
        )