import os

#import pyaudio

# Audio settings
#AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1
AUDIO_RATE = 16000
AUDIO_CHUNK = int(AUDIO_RATE * 0.5)   # 0.5 seconds

# Optional: specify input device index (None = auto-detect)
MICROPHONE_DEVICE_INDEX = None

# Confidence threshold for wake word
WAKE_WORD_THRESHOLD = 0.5

# Whisper settings
WHISPER_MODEL_SIZE = "base"           # tiny, base, small, medium, large
WHISPER_LANGUAGE = "ru"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# Recording parameters
RECORDING_MAX_DURATION = 10
RECORDING_SILENCE_THRESHOLD = 500     # RMS
RECORDING_SILENCE_CHUNKS = 4

# Ollama LLM settings
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:e4b")
OLLAMA_TIMEOUT = 600

# Web search (fallback when the LLM can't answer)
WEB_SEARCH_MAX_RESULTS = 5
