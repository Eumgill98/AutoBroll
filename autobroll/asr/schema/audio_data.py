from __future__ import annotations
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, ConfigDict, model_validator

import numpy as np
import tempfile
import ffmpeg

class AudioData(BaseModel):
    """
    A class to manage audio data.

    Fields:
        path: audio file path
        waveform: audio waveform as a numpy array
        sample rate: sample rate of the audio in Hz
        temp_file: flag indicating if this is a temporary file
    """
    path: Optional[Path] = None
    waveform: Optional[np.ndarray] = None
    sample_rate: Optional[int] = None
    temp_file: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def _validate_audio_data(self):
        """
        Validate AudioData instance after initialization.
        Ensures either path or waveform is provided, and sample_rate is set when waveform is used.
        """
        if self.path is None and self.waveform is None:
            raise ValueError("Either path or waveform must be provided") 
        if self.waveform is not None and self.sample_rate is None: 
            raise ValueError("sample_rate required when waveform is provided")
        return self
    
    @classmethod
    def from_audio(
        cls,
        path: Path,
    ) -> AudioData:
        """
        Create an AudioData instance from an audio file path.
        
        Args:
            path: Path to the audio file
            
        Returns:
            AudioData: A new AudioData instance
            
        Raises:
            FileNotFoundError: If the audio file does not exist
        """
        if not path.exists():
            raise FileNotFoundError(path)
        
        return cls(
            path=path,
            temp_file=False,
        )
    
    @classmethod
    def from_video(
        cls,
        path: Path,
        sample_rate:int = 16000,
        mono:bool = True,
        temp:bool = True,
    ) -> AudioData:
        """
        Extract audio from a video file and create an AudioData instance.
        
        Args:
            path: Path to the video file
            sample_rate: Target sample rate in Hz (default: 16000)
            mono: If True, extract mono audio; if False, stereo (default: True)
            temp: If True, save to temporary file; if False, return waveform in memory (default: True)
            
        Returns:
            AudioData: A new AudioData instance with extracted audio
            
        Raises:
            FileNotFoundError: If the video file does not exist
        """
        if not path.exists():
            raise FileNotFoundError(path)
        
        if temp:
            tmp = tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            )

            (
                ffmpeg
                .input(str(path))
                .output(
                    tmp.name,
                    format="wav",
                    ac=1 if mono else 2,
                    ar=sample_rate,
                )
                .overwrite_output()
                .run(quiet=True)
            )

            return cls(
                path=Path(tmp.name),
                temp_file=True,
            )


        out, _ = (
            ffmpeg
            .input(str(path))
            .output(
                "pipe:",
                format="f32le",
                ac=1 if mono else 2,
                ar=sample_rate,
            )
            .run(
                capture_stdout=True,
                capture_stderr=True,
                quiet=True,
            )
        )

        waveform = np.frombuffer(out, dtype=np.float32)

        if not mono:
            waveform = waveform.reshape(-1, 2)

        return cls(
            waveform=waveform,
            sample_rate=sample_rate,
            temp_file=False,
        )
    
    def cleanup(self):
        """
        Clean up temporary audio file if it exists.
        Should be called when the AudioData instance is no longer needed.
        """
        if self.temp_file and self.path and self.path.exists():
            self.path.unlink()