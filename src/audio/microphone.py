import sounddevice as sd
import numpy as np
from config import (
    AUDIO_RATE, AUDIO_CHUNK,
    RECORDING_MAX_DURATION, RECORDING_SILENCE_THRESHOLD, RECORDING_SILENCE_CHUNKS
)

class Microphone:
    def __init__(self, device_index=None):
        self.device_index = device_index
        self.sample_rate = AUDIO_RATE
        self.chunk = AUDIO_CHUNK

        if device_index is not None:
            sd.default.device = device_index

        try:
            default_input = sd.default.device
            if isinstance(default_input, tuple):
                default_input = default_input[0]
            info = sd.query_devices(default_input, 'input')
            print(f"Microphone: using '{info['name']}' (index {default_input})")
        except Exception as e:
            print(f"Warning: could not determine default input device: {e}")

    def get_chunk(self):
        """Read one audio chunk as a numpy array of int16."""
        audio = sd.rec(
            int(self.chunk),
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            blocking=True
        )
        sd.wait()
        return audio.flatten()

    def record_until_silence(self, max_duration=RECORDING_MAX_DURATION,
                             silence_threshold=RECORDING_SILENCE_THRESHOLD,
                             silence_chunks=RECORDING_SILENCE_CHUNKS,
                             verbose=False):
        """
        Record audio until silence is detected.
        Returns raw PCM bytes (int16).
        """
        frames = []
        silent_count = 0
        max_chunks = int(max_duration * self.sample_rate / self.chunk)

        if verbose:
            print("Listening... (speak now)")

        for _ in range(max_chunks):
            chunk = self.get_chunk()
            frames.append(chunk.tobytes())

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
        pass