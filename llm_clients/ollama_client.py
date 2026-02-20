import requests
from .base import BaseLLM

class OllamaClient(BaseLLM):
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.base_url = "http://localhost:11434/api/chat"

    def generate(self, system_prompt: str, user_prompt: str) -> str:

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()

        return response.json()["message"]["content"]