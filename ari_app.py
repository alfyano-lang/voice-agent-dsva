import ari
import logging
import os
import time
from dotenv import load_dotenv
from llm_service import LLMService
from tts_service import TTSService

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
ASTERISK_HOST = os.getenv("ASTERISK_HOST", "localhost")
ASTERISK_PORT = int(os.getenv("ASTERISK_PORT", 8088))
ASTERISK_USER = os.getenv("ASTERISK_USER", "asterisk")
ASTERISK_PASS = os.getenv("ASTERISK_PASS", "asterisk")
APP_NAME = os.getenv("ASTERISK_APP_NAME", "voice-agent")

class VoiceAgentApp:
    def __init__(self):
        self.client = ari.connect(
            f"http://{ASTERISK_HOST}:{ASTERISK_PORT}", 
            ASTERISK_USER, 
            ASTERISK_PASS
        )
        self.llm = LLMService()
        self.tts = TTSService()
        self.conversation_history = {} # Key: channel.id, Value: list of messages

    def start(self):
        logger.info(f"Starting ARI Application: {APP_NAME}")
        self.client.on_channel_event('StasisStart', self.on_stasis_start)
        self.client.on_channel_event('StasisEnd', self.on_stasis_end)
        self.client.run(apps=APP_NAME)

    def on_stasis_start(self, channel, event):
        logger.info(f"Channel {channel.id} entered Stasis")
        channel.answer()
        
        # Initialize history for this channel
        self.conversation_history[channel.id] = []
        
        # Initial Greeting
        self.process_turn(channel, "Hello, this is Alex. How can I help you today?")

    def on_stasis_end(self, channel, event):
        logger.info(f"Channel {channel.id} left Stasis")
        if channel.id in self.conversation_history:
            del self.conversation_history[channel.id]

    def process_turn(self, channel, ai_text):
        # 1. Generate Audio
        logger.info(f"AI Response: {ai_text}")
        audio_file = f"/tmp/response_{channel.id}_{int(time.time())}.mp3"
        
        # In a real Asterisk setup, the file needs to be accessible by Asterisk.
        # Often this means writing to /var/lib/asterisk/sounds/ or a shared mount.
        # For this template, we assume /tmp is shared or we use a playback URL.
        # Note: ElevenLabs returns MP3, Asterisk usually prefers WAV (16bit 8khz).
        # You might need ffmpeg conversion here.
        
        generated_path = self.tts.generate_audio_file(ai_text, audio_file)
        
        if generated_path:
            # 2. Play Audio
            # 'sound:' prefix usually looks in Asterisk sound dir. 
            # To play absolute path, might need specific configuration or 'file:' prefix depending on modules.
            # We will use a placeholder playback.
            playback = channel.play(media=f"sound:{generated_path[:-4]}") # Remove extension for Asterisk sound resource
            
            # Wait for playback to finish (simplified)
            # In real ARI, you'd listen for PlaybackFinished event.
            time.sleep(2) # Mock wait
            
        # 3. Record / Listen for User Input
        # This is where you would trigger recording or connect to a stream for STT.
        # For this template, we will simulate a "listen" phase.
        user_text = self.mock_listen(channel)
        
        if user_text:
            # 4. Update History & Get LLM Response
            self.conversation_history[channel.id].append({"role": "assistant", "content": ai_text})
            self.conversation_history[channel.id].append({"role": "user", "content": user_text})
            
            if "hangup" in user_text.lower():
                channel.hangup()
                return

            response_text = self.llm.get_response(self.conversation_history[channel.id])
            
            if response_text == "transfer_to_owner":
                # Handle transfer logic
                logger.info("Transferring call...")
                channel.continueInDialplan(context="default", extension="1000", priority=1)
            else:
                self.process_turn(channel, response_text)

    def mock_listen(self, channel):
        """
        Placeholder for STT logic. 
        In production, this would record audio -> send to STT API -> return text.
        """
        logger.info("Listening... (Mocking user input)")
        time.sleep(1)
        # Randomly return a query for demonstration if this were running
        return None # Return None to stop the loop in this static analysis

if __name__ == "__main__":
    # Wait for Asterisk to be ready
    time.sleep(2)
    try:
        app = VoiceAgentApp()
        app.start()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
