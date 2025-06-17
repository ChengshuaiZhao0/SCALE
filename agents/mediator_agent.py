from .base_agent import BaseAgent
from typing import List

class MediatorAgent(BaseAgent):
    """An agent that mediates codebook update discussions."""
    def __init__(self, api_key: str, model: str, prompt_template: str):
        super().__init__(api_key, model, prompt_template)

    def mediate(self, proposals: List[str]) -> str:
        """Summarizes proposals and asks for agreement."""
        self.reset_context()
        
        mediate_prompt = "Here are the proposed CODEBOOK from other social scientists:\n\n"
        for i, proposal in enumerate(proposals):
            mediate_prompt += f"Agent {i+1}'s proposal:\n{proposal}\n\n"
        
        self.add_user_message(mediate_prompt)
        
        summary = self._generate_answer()
        self.add_assistant_message(summary)
        
        self.reset_context() # Reset after each mediation
        return summary