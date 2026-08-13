import pyaudio
import numpy as np
from config import (
    AUDIO_FORMAT, AUDIO_CHANNELS, AUDIO_RATE, AUDIO_CHUNK,
    RECORDING_MAX_DURATION, RECORDING_SILENCE_THRESHOLD, RECORDING_SILENCE_CHUNKS
)

class Microphone:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=AUDIO_FORMAT,
            channels=AUDIO_CHANNELS,
            rate=AUDIO_RATE,
            input=True,
            frames_per_buffer=AUDIO_CHUNK
        )

    def get_chunk(self):
        """Read one audio chunk as a numpy array of int16."""
        try:
            data = self.stream.read(AUDIO_CHUNK, exception_on_overflow=False)
            return np.frombuffer(data, dtype=np.int16)
        
        except Exception:
            return np.zeros(AUDIO_CHUNK, dtype=np.int16)

    def record_until_silence(self, max_duration=RECORDING_MAX_DURATION,
                             silence_threshold=RECORDING_SILENCE_THRESHOLD,
                             silence_chunks=RECORDING_SILENCE_CHUNKS,
                             verbose=False):
        """
        Record audio until silence is detected.
        Returns raw PCM bytes (int16). 
        If verbose=False, no console output is produced.
        """
        frames = []
        silent_count = 0
        recorded_chunks = 0
        max_chunks = int(max_duration * AUDIO_RATE / AUDIO_CHUNK)

        if verbose:
            print("Listening... (speak now)")

        while recorded_chunks < max_chunks:
            chunk = self.get_chunk()
            frames.append(chunk.tobytes())
            recorded_chunks += 1

            rms = np.sqrt(np.mean(chunk.astype(np.float32)**2))
            if rms < silence_threshold:
                silent_count += 1
            else:
                silent_count = 0

            if silent_count >= silence_chunks:
                if verbose:
                    print("Silence detected, recording stopped.")
                break

        return b''.join(frames)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
