import tempfile
import wave
import os
from faster_whisper import WhisperModel
from .interface import Recognizer
from config import WHISPER_MODEL_SIZE, WHISPER_LANGUAGE, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE

class WhisperRecognizer(Recognizer):
    def __init__(self, model_size=WHISPER_MODEL_SIZE,
                 device=WHISPER_DEVICE,
                 compute_type=WHISPER_COMPUTE_TYPE,
                 language=WHISPER_LANGUAGE):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.language = language

    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000,
                   channels: int = 1, sample_width: int = 2) -> str:
        if not audio_bytes:
            return ""

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name

        try:
            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_bytes)

            segments, _ = self.model.transcribe(
                temp_path,
                language=self.language,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            full_text = " ".join(seg.text for seg in segments)
            return full_text.strip()
        
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
