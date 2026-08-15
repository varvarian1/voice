import torch
import torch.hub
import pygame
import numpy as np

class Speaker:
    def __init__(self, language='ru', speaker='ruslan_v2', device='cpu', sample_rate=16000):
        """ Initialize the TTS model. """
        self.language = language
        self.speaker = speaker
        self.device = torch.device(device)
        self.sample_rate = sample_rate

        # Load the Silero model from torch.hub (it will be cached after first download)
        # The hub returns: model, example_text (we ignore the example text)
        self.model, self.example_text = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language=self.language,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
            device=self.device,
            trust_repo=True # Silero repository is trusted
        )

    def say(self, text: str):
        """ Synthesize the given text and play it through the speakers. """
        if not text:
            return
        
        try:
            # Generate audio from text using the loaded model
            # The returned value can be a torch.Tensor, a list, or a numpy array
            audio = self.model.apply_tts(text, self.sample_rate)

            # Ensure audio is a numpy array of float32
            if isinstance(audio, torch.Tensor):
                audio = audio.cpu().numpy().astype(np.float32)
            elif isinstance(audio, list):
                audio = np.array(audio, dtype=np.float32)
            else:
                audio = np.array(audio, dtype=np.float32)

            if audio.size == 0:
                print("TTS: empty audio")
                return

            """
            Normalize the audio to the range [-1, 1] and convert to int16.
            Pygame expects 16‑bit PCM (int16) values.
            """
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                audio_int16 = np.int16(audio / max_val * 32767)
            else:
                audio_int16 = np.int16(audio)

            # Ensure the array is 1‑dimensional (mono channel)
            audio_int16 = audio_int16.flatten()

            """
            Initialize pygame mixer with the correct sample rate,
            16‑bit signed integer, and mono channel
            """
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1)

            # Create a Sound object from the int16 array and play it
            sound = pygame.sndarray.make_sound(audio_int16)
            sound.play()

            # Wait until the playback finishes before continuing
            while pygame.mixer.get_busy():
                continue

            pygame.mixer.quit()

        except Exception as e:
            print(f"TTS Error: {e}")
            import traceback
            traceback.print_exc()

    def stop(self):
        """ Stop any currently playing speech immediately. """
        pygame.mixer.music.stop()