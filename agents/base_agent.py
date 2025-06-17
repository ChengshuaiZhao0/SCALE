import time
from typing import List, Dict, Any
from openai import OpenAI

class BaseAgent:
    """A base class for all AI-powered agents."""
    def __init__(self, api_key: str, model: str, system_prompt: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.context: List[Dict[str, str]] = [{"role": "system", "content": self.system_prompt}]

    def _generate_answer(self, temperature: float = 0.0) -> str:
        """
        Generates a response from the LLM based on the current context.
        Includes retry logic for API errors.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.context,
                n=1,
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Retrying due to an error: {e}")
            time.sleep(20)
            return self._generate_answer(temperature)

    def add_user_message(self, content: str):
        """Adds a user message to the agent's context."""
        self.context.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        """Adds an assistant message to the agent's context."""
        self.context.append({"role": "assistant", "content": content})
        
    def get_last_response(self) -> str:
        """Returns the last assistant response from the context."""
        for message in reversed(self.context):
            if message["role"] == "assistant":
                return message["content"]
        return ""

    def reset_context(self):
        """Resets the conversation context to just the system prompt."""
        self.context = [{"role": "system", "content": self.system_prompt}]