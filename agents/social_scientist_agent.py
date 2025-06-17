from .base_agent import BaseAgent
from typing import List, Dict

class SocialScientistAgent(BaseAgent):
    """Represents an LLM agent emulating a social scientist."""
    def __init__(self, api_key: str, model: str, persona: str, codebook: str):
        self.persona = persona
        self.codebook = codebook
        # system_prompt = f"Persona:\n{persona}\n\nCODEBOOK:\n{codebook}\n\nINSTRUCTION:\n{instruction}"
        system_prompt = f"Persona:\n{persona}\n\nCODEBOOK:\n{codebook}"
        super().__init__(api_key, model, system_prompt)

    def code_text(self, text: str) -> str:
        """Codes a single piece of text based on the codebook and persona."""
        coding_prompt = f"TEXT:\n{text}"
        self.add_user_message(coding_prompt)
        response = self._generate_answer()
        self.add_assistant_message(response)
        return response

    def discuss(self, text: str, your_answer: str, other_answers: List[str]) -> str:
        """Participates in a discussion to resolve coding disagreements."""
        other_answers_formatted = "\n\n".join(
            [f"Another agent's response:\n{ans}" for ans in other_answers]
        )
        discussion_prompt = (
            f"TEXT:\n{text}\n\n"
            f"YOUR PREVIOUS ANSWER:\n{your_answer}\n\n"
            f"RESPONSES FROM OTHERS:\n{other_answers_formatted}"
        )
        self.add_user_message(discussion_prompt)
        response = self._generate_answer()
        self.add_assistant_message(response)
        return response

    def receive_intervention(self, intervention_prompt: str) -> str:
        """
        Processes an intervention prompt from a human expert and generates a new response.
        This allows the agent's behavior to be guided mid-task.
        """
        self.add_user_message(intervention_prompt)
        response = self._generate_answer()
        self.add_assistant_message(response)
        return response

    def propose_codebook_update(self, orginal_codebook) -> str:
        """Proposes changes to the codebook based on recent analysis."""
        update_prompt = (
            f"ORIGINAL CODEBOOK:\n{orginal_codebook}"
        )
        self.add_user_message(update_prompt)
        response = self._generate_answer()
        self.add_assistant_message(response)
        return response

    def review_mediated_codebook(self, mediator_summary: str) -> str:
        """Reviews the summary from the Mediator and provides a final opinion."""
        self.add_user_message(mediator_summary)
        response = self._generate_answer()
        self.add_assistant_message(response)
        return response
        
    def update_codebook(self, new_codebook: str):
        """Updates the agent's internal codebook and resets the context for the next round."""
        self.codebook = new_codebook
        self.system_prompt = f"Persona:\n{self.persona}\n\nCODEBOOK:\n{new_codebook}"
        # Resets the context to start fresh with the new system prompt
        self.reset_context()