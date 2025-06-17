class HumanExpert:
    """Handles the human-in-the-loop intervention process."""
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt

    def intervene(self) -> str:
        """
        Prompts the human for intervention and returns the formatted prompt.
        """
        content = input(
            f'Type your intervention (press enter to skip):\n\n'
        )

        if not content.strip():
            return None
        
        intervention_prompt = f"{self.system_prompt}\n\nFeedback:\n{content}"
        return intervention_prompt