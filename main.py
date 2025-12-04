import os
import sys
from llm_service import LLMService
from tts_service import TTSService

def main():
    print("Initializing Alex (DSVA) - CLI Mode...")
    
    # Check for API Keys
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment.")
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("Warning: ELEVENLABS_API_KEY not found in environment.")

    try:
        llm = LLMService()
        tts = TTSService()
    except Exception as e:
        print(f"Error initializing services: {e}")
        return

    history = []
    
    print("\n[System] Call connected. (Type 'hangup' to end)")
    
    while True:
        try:
            user_input = input("\n[Caller]: ")
            if user_input.lower() in ["hangup", "exit", "quit"]:
                print("[System] Call ended.")
                break
            
            # Update history
            history.append({"role": "user", "content": user_input})
            
            # Get LLM Response
            print("[Alex]: Thinking...")
            response_text = llm.get_response(history)
            
            if response_text == "transfer_to_owner":
                print(f"\n[Alex]: {response_text}")
                print("[System] Initiating transfer sequence...")
                break
            else:
                print(f"\n[Alex]: {response_text}")
                history.append({"role": "assistant", "content": response_text})
                
                # Generate Audio
                print("[System] Generating audio...")
                audio_path = tts.generate_audio_file(response_text, "response.mp3")
                if audio_path:
                    print(f"[System] Audio saved to {audio_path}")
                else:
                    print("[System] Audio generation failed.")
                
        except KeyboardInterrupt:
            print("\n[System] Call interrupted.")
            break

if __name__ == "__main__":
    main()
