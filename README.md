# Voice App - Digital Services Voice Agent (DSVA)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Asterisk](https://img.shields.io/badge/Asterisk-ARI-orange?style=for-the-badge&logo=asterisk)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green?style=for-the-badge&logo=openai)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-TTS-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

**Alex** is a high-performance, low-latency voice agent designed for real-time telephony environments. Built with Python and Asterisk, it leverages state-of-the-art LLMs and Text-to-Speech engines to deliver natural, professional customer interactions.

---

## 🚀 Features

-   **Real-time Telephony Integration**: Seamless connection with Asterisk via ARI (Asterisk REST Interface).
-   **Intelligent Conversation**: Powered by OpenAI's GPT-4o for context-aware, professional dialogue.
-   **Ultra-Realistic Voice**: Utilizes ElevenLabs Turbo v2.5 for human-like speech synthesis with minimal latency.
-   **Secure & Scalable**: Environment-based configuration and modular architecture designed for production.

## 🛠️ Architecture

The system operates on a modular architecture:
1.  **Telephony Layer**: Asterisk handles the SIP/RTP stream.
2.  **Control Layer**: Python application (`ari_app.py`) manages the call state via ARI.
3.  **Cognitive Layer**: `LLMService` processes user intent and generates responses.
4.  **Synthesis Layer**: `TTSService` converts text to audio in real-time.

## 📦 Installation

### Prerequisites
-   Python 3.9+
-   Asterisk 16+ (configured for ARI)
-   API Keys for OpenAI and ElevenLabs

### Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/voice-app.git
    cd voice-app
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Copy the example configuration and add your secure keys.
    ```bash
    cp .env.example .env
    # Edit .env with your API keys and Asterisk credentials
    ```

## 🚦 Usage

### CLI Simulation Mode
Test the agent logic and voice synthesis without a telephony server.
```bash
python main.py
```

### Production Mode (ARI)
Start the Asterisk control application.
```bash
python ari_app.py
```

## 🔒 Security

This project adheres to strict security practices:
-   **No Hardcoded Secrets**: All sensitive keys are managed via environment variables.
-   **Input Sanitization**: Basic input handling is implemented (expandable for production).
-   **Logging**: structured logging is used; ensure logs are rotated and secured in production.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
