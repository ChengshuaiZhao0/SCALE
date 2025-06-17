from .base_agent import BaseAgent
from typing import List

class JudgeAgent(BaseAgent):
    """An agent that judges whether other agents are in agreement."""
    def __init__(self, api_key: str, model: str, prompt_template: str):
        super().__init__(api_key, model, prompt_template)

    def check_agreement(self, agent_responses: List[str]) -> bool:
        """
        Compares agent responses and judges if they are the same.
        Returns True for agreement, False for disagreement.
        """
        self.reset_context()
        
        check_prompt = "Here are the answer from other social scientists:\n\n"
        for i, response in enumerate(agent_responses):
            check_prompt += f"Agent {i+1} response:\n{response}\n\n"
        
        self.add_user_message(check_prompt)
        
        judgement = self._generate_answer()
        self.add_assistant_message(judgement)
        
        self.reset_context() # Reset after each judgment
        
        return "same" in judgement.lower() and "different" not in judgement.lower()