import sys
import signal
import json
from audio.microphone import Microphone
from speech.whisper_recognizer import WhisperRecognizer
from tts.speaker import Speaker
from config import AUDIO_RATE, AUDIO_CHANNELS, SAMPLE_WIDTH, MICROPHONE_DEVICE_INDEX
from vosk import Model, KaldiRecognizer

VOSK_MODEL_PATH = "models/vosk-model-ru/vosk-model-small-ru-0.22"
KEYWORDS = ["оли", "олли", "оливер", " олливер", "olli", "oli"] # variants

def main():
    mic = Microphone(device_index=MICROPHONE_DEVICE_INDEX)
    recognizer = WhisperRecognizer()
    speaker = Speaker()

    # Load Vosk model
    vosk_model = Model(VOSK_MODEL_PATH)
    vosk_recognizer = KaldiRecognizer(vosk_model, AUDIO_RATE)
    vosk_recognizer.SetWords(True)

    def signal_handler(sig, frame):
        mic.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    print("Ready. (showing all partial recognitions, activate on keyword)")
    try:
        while True:
            chunk = mic.get_chunk()
            vosk_recognizer.AcceptWaveform(chunk.tobytes())

            # Get partial result
            partial = json.loads(vosk_recognizer.PartialResult())
            text = partial.get("partial", "")
            if text:
                print(f"Partial: {text}")
                #speaker.say(text)

                # Check for keywords
                text_lower = text.lower()
                if any(kw in text_lower for kw in KEYWORDS):
                    # Keyword detected -> record command
                    audio_bytes = mic.record_until_silence(verbose=False)
                    if len(audio_bytes) >= AUDIO_RATE * 0.5:
                        transcribed = recognizer.transcribe(
                            audio_bytes,
                            sample_rate=AUDIO_RATE,
                            channels=AUDIO_CHANNELS,
                            sample_width=SAMPLE_WIDTH
                        )
                        if transcribed:
                            print(f"Command: {transcribed}") # final output
                            speaker.say(transcribed)
                    # Optional: small delay to avoid re-triggering
                    # import time; time.sleep(0.5)
                    
    except Exception:
        pass

    finally:
        mic.close()

if __name__ == "__main__":
    main()