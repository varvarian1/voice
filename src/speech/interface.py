from abc import ABC, abstractmethod

class Recognizer(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000,
                   channels: int = 1, sample_width: int = 2) -> str:
        """Convert raw PCM audio to text."""
        pass
