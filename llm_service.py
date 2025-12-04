import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import ALEX_SYSTEM_PROMPT

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = ALEX_SYSTEM_PROMPT

    def get_response(self, conversation_history):
        """
        Generates a response from the LLM based on the conversation history.
        
        Args:
            conversation_history (list): List of dicts [{"role": "user", "content": "..."}, ...]
        
        Returns:
            str: The text response from the LLM.
        """
        messages = [{"role": "system", "content": self.system_prompt}] + conversation_history
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # Or gpt-3.5-turbo for lower latency
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return "I apologize, but I am having trouble processing your request right now."
