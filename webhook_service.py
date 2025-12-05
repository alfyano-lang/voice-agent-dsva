import json
import os
import requests
import logging

logger = logging.getLogger(__name__)
CONFIG_FILE = "config.json"

class WebhookService:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                self.config = {}
        else:
            self.config = {}

    def get_webhook_url(self):
        return self.config.get("webhook_url", "")

    def get_output_format(self):
        return self.config.get("output_format", "standard")

    def set_config(self, url, output_format):
        self.config["webhook_url"] = url
        self.config["output_format"] = output_format
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def send_data(self, event_type, payload):
        url = self.get_webhook_url()
        fmt = self.get_output_format()
        
        if not url:
            return None

        try:
            # Format Data
            if fmt == "flat":
                data = payload.copy()
                data["event"] = event_type
            else: # standard
                data = {
                    "event": event_type,
                    "data": payload
                }

            response = requests.post(url, json=data, timeout=5)
            response.raise_for_status()
            
            # Try to parse response
            try:
                return response.json()
            except:
                return {"raw_response": response.text}

        except Exception as e:
            logger.error(f"Failed to send webhook: {e}")
            return None
