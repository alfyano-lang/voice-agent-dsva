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

    def set_webhook_url(self, url):
        self.config["webhook_url"] = url
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def send_data(self, event_type, payload):
        url = self.get_webhook_url()
        if not url:
            logger.info("No webhook URL configured. Skipping webhook trigger.")
            return False

        try:
            data = {
                "event": event_type,
                "data": payload
            }
            response = requests.post(url, json=data, timeout=5)
            response.raise_for_status()
            logger.info(f"Webhook sent successfully to {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to send webhook: {e}")
            return False
