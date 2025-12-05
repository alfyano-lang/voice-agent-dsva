import os
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# Import our services
from llm_service import LLMService
from ari_app import VoiceAgentApp
from webhook_service import WebhookService
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

app = FastAPI(title="Alex DSVA Dashboard")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
llm_service = LLMService()
webhook_service = WebhookService()

# Models
class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str

class ConfigRequest(BaseModel):
    webhook_url: str

# API Endpoints
@app.get("/api/config")
async def get_config():
    return {"webhook_url": webhook_service.get_webhook_url()}

@app.post("/api/config")
async def update_config(config: ConfigRequest):
    success = webhook_service.set_webhook_url(config.webhook_url)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save configuration")
    return {"status": "updated", "webhook_url": config.webhook_url}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Construct history for LLM
        conversation = request.history + [{"role": "user", "content": request.message}]
        response_text = llm_service.get_response(conversation)
        
        # Check if we should trigger webhook based on response content
        # In a real app, the LLM might return structured data or a specific flag.
        # Here we use simple keyword matching from the prompt logic.
        if "logged your request" in response_text or "transfer_to_owner" in response_text:
            webhook_service.send_data("interaction_logged", {
                "user_message": request.message,
                "agent_response": response_text,
                "source": "web_simulator"
            })

        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Chat API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve Frontend
# Mount the 'frontend' directory to root '/'
# We need to make sure index.html is served at root.
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

def start_ari():
    """Starts the Asterisk ARI application in a separate thread."""
    try:
        logger.info("Starting ARI Application in background...")
        # Check if Asterisk config is present before trying to connect to avoid crash loops in dev
        if os.getenv("ASTERISK_HOST"):
            voice_app = VoiceAgentApp()
            voice_app.start()
        else:
            logger.warning("ASTERISK_HOST not set. ARI App not started.")
    except Exception as e:
        logger.error(f"ARI App failed to start: {e}")

if __name__ == "__main__":
    # Start ARI in background thread
    ari_thread = threading.Thread(target=start_ari, daemon=True)
    ari_thread.start()

    # Start Web Server
    # Host 0.0.0.0 is important for Docker
    uvicorn.run(app, host="0.0.0.0", port=8000)
