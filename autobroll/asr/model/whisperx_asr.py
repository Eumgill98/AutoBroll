from typing import Optional, Dict, Any
import whisperx

from autobroll.asr.base import BaseASR
from autobroll.asr.schema import AudioData

class WhisperXASR(BaseASR):
    """
    WhisperX-based ASR class.
    """
    def __init__(
        self,
        model_name: str = "large-v2",
        device: str = "cpu",
        compute_type: str = "float16",
        language: Optional[str] = None,
        batch_size: int = 16
    ):
        """
        Initialize the WhisperX ASR engine.

        Args:
            model_name (str): Whisper model identifier
                (e.g. "base", "small", "medium", "large-v2")
            device (str): Execution device ("cpu", "cuda")
            compute_type (str): Model compute precision (e.g. "float16", "int8")
            language (Optional[str]): Target language code (None for auto-detection)
            batch_size (int): Batch size used during transcription inference
        """
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.language = language
        self.batch_size = batch_size
        
        self.model = whisperx.load_model(
            self.model_name,
            device=self.device,
            compute_type=self.compute_type,
            language=self.language,
        )

    def transcribe(
        self,
        audio: AudioData,
    ) -> Dict[str, Any]:
        """
        Transcribe audio using WhisperX.

        Args:
            audio (AudioData): Input audio data.
        
        Returns:
            Dict[str, Any]: Transcription result containing:
                - language: detected or specified language
                - segments: aligned transcription segments with timestamps
        """
        # load data
        if audio.path is not None:
            waveform = whisperx.load_audio(str(audio.path))
            sample_rate = 16000
        elif audio.waveform is not None:
            waveform = audio.waveform
            sample_rate = audio.sample_rate
        else:
            raise ValueError("Invalid AudioData!")

        result = self.model.transcribe(
            waveform,
            batch_size=self.batch_size,
        )

        align_model, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=self.device,
        )

        aligned = whisperx.align(
            result["segments"],
            align_model,
            metadata,
            waveform,
            sample_rate,
            device=self.device,
        )

        return {
            "language": result["language"],
            "segments": aligned["segments"],
        }