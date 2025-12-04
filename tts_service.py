import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv

load_dotenv()

class TTSService:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb") # Default to a standard voice if not set

    def generate_audio_file(self, text, output_path="output.mp3"):
        """
        Generates audio from text using ElevenLabs and saves it to a file.
        
        Args:
            text (str): The text to convert to speech.
            output_path (str): The path to save the audio file.
            
        Returns:
            str: The path to the saved audio file, or None if failed.
        """
        try:
            audio = self.client.generate(
                text=text,
                voice=self.voice_id,
                model="eleven_turbo_v2_5" # Low latency model
            )
            save(audio, output_path)
            return output_path
        except Exception as e:
            print(f"Error calling ElevenLabs: {e}")
            return None
