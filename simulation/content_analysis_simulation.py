import pandas as pd
import os
from typing import List, Dict, Any

from agents.social_scientist_agent import SocialScientistAgent
from agents.judge_agent import JudgeAgent
from agents.mediator_agent import MediatorAgent
from agents.human_expert import HumanExpert
from utils.logger import Logger
from utils.config_loader import load_codebook

class ContentAnalysisSimulation:
    def __init__(self, config: Dict[str, Any], logger: Logger):
        self.config = config
        self.logger = logger
        
        # Simulation parameters
        self.num_agents = config['settings']['agents']
        self.discussion_rounds = config['settings']['rounds']
        self.chunk_size = config['settings']['chunk_size']
        self.model = config['settings']['model']

        # Load data
        data_file = os.path.join(config['paths']['data_path'], config['dataset_name'], 'data.xlsx')
        df = pd.read_excel(data_file)
        self.text_chunks = [df['Text'][i:i + self.chunk_size] for i in range(0, len(df), self.chunk_size)]

        # Coder Simulation
        self.logger.log("********** Bot Annotation **********\n")
        self.api_key = config['api_key']
        self.codebook = load_codebook(config['dataset_name'], config['paths']['data_path'])
        
        self.scientists = self._create_scientists()
        self.judge = JudgeAgent(self.api_key, self.model, config['prompt']['judge'])
        self.mediator = MediatorAgent(self.api_key, self.model, config['prompt']['mediator'])
        self.logger.log(f"Initialized {self.num_agents} Social Scientist Agents For {self.config['dataset_name']} Task.\n")

        # Intervention settings
        self.intervention_settings = config['settings'].get('intervention', {})
        self.intervention_enabled = self.intervention_settings.get('enabled', False)
        if self.intervention_enabled:
            self.intervention_scope = self.intervention_settings.get('scope', 'targeted')
            self.intervention_authority = self.intervention_settings.get('authority', 'collaborative')
            self.human_expert = HumanExpert(system_prompt=config['prompt'][self.intervention_authority])
        else:
            self.human_expert = None
        

    def _create_scientists(self) -> List[SocialScientistAgent]:
        """Initializes the SocialScientistAgent instances."""
        scientists = []
        personas = list(self.config['persona'].values())
        for i in range(self.num_agents):
            agent = SocialScientistAgent(
                api_key=self.api_key,
                model=self.model,
                persona=personas[i],
                codebook=self.codebook,
            )
            scientists.append(agent)
        return scientists


    def _human_intervention(self, phase: str) -> str:
        # *** HUMAN INTERVENTION POINT (DISCUSSION) ***
        intervention_prompt = self.human_expert.intervene()
        if intervention_prompt:
            self.logger.log(f"!!! {self.intervention_authority.upper()} Intervention on {phase} Activated !!!\n")
            self.logger.log(f"Intervention Prompt:\n{intervention_prompt}\n")
            intervened_responses = [agent.receive_intervention(intervention_prompt) for agent in self.scientists]
            for k, response in enumerate(intervened_responses):
                self.logger.log(f"Agent {k+1} {phase} (Post-Intervention): {response}\n")

            return intervened_responses
        else:
            self.logger.log(f"No intervention provided for {phase}. Continuing without changes.\n")
            return None


    def run(self):
        """Runs the entire content analysis simulation loop."""
        full_log = []
        for i, chunk in enumerate(self.text_chunks):
            self.logger.log(f"===== Processing Chunk {i+1}/{len(self.text_chunks)} =====\n")
            
            # Bot Annotation
            coding_results, coding_agreements = self._run_coding_phase(chunk)
            
            # Agent Discussion
            discussion_results, final_answers, final_agreements = self._run_discussion_phase(chunk, coding_results, coding_agreements)
            
            # Codebook Evolution
            self._run_codebook_evolution_phase()
            
            # Log results for this chunk
            chunk_log = {
                "chunk_id": i,
                "coding_phase": {"results": coding_results, "agreements": coding_agreements},
                "discussion_phase": {"history": discussion_results, "results": final_answers, "agreements": final_agreements},
                "final_codebook": self.codebook
            }
            full_log.append(chunk_log)
            self.logger.save_json(chunk_log, f'chunk_{i}_results.json')
        
        self.logger.save_json(full_log, 'full_simulation_log.json')
        self.logger.log("===== Simulation Complete =====\n")

    def _run_coding_phase(self, chunk: pd.Series):
        self.logger.log("********** Bot Annotation **********\n")

        for agent in self.scientists:
            agent.add_user_message(self.config['prompt']['coding'])
    
        coding_results = {}
        coding_agreements = {}

        self.logger.log("--- Agents Coding Texts ---\n")
        for i, text in enumerate(chunk):
            text_id = f"Text-{chunk.index[i]+1}"
            self.logger.log(f"--- Coding {text_id} ---\n{text}\n")
            
            responses = [agent.code_text(text) for agent in self.scientists]
            for j, response in enumerate(responses):
                self.logger.log(f"Agent {j+1}: {response}\n")

            coding_results[text_id] = responses
            agreement = self.judge.check_agreement(responses)
            coding_agreements[text_id] = agreement
            self.logger.log(f"Judge's Verdict: {'Agreement' if agreement else 'Disagreement'}\n")

        return coding_results, coding_agreements

    def _run_discussion_phase(self, chunk: pd.Series, coding_results: Dict, coding_agreements: Dict):
        self.logger.log("********** Agent Discussion **********\n")

        for agent in self.scientists:
            agent.add_user_message(self.config['prompt']['discussion'])

        discussion_results = {}
        final_answers = {}
        final_agreements = {}

        self.logger.log("\n--- Agents Discussing Disagreements ---\n")
        for i, text in enumerate(chunk):
            text_id = f"Text-{chunk.index[i]+1}"
            if not coding_agreements[text_id]:
                self.logger.log(f"\n--- Discussing {text_id} ---\n")
                discussion_history = [coding_results[text_id]]

                for round_num in range(self.discussion_rounds):
                    self.logger.log(f"<Discussion Round {round_num + 1}>\n")
                    current_answers = discussion_history[-1]

                    next_round_answers = [agent.discuss(text, current_answers[j], current_answers[:j] + current_answers[j+1:])
                                          for j, agent in enumerate(self.scientists)]
                    for j, answer in enumerate(next_round_answers):
                        self.logger.log(f"Agent {j+1}: {answer}\n")
                    
                    # *** HUMAN INTERVENTION POINT (DISCUSSION) ***
                    if self.intervention_enabled:
                        intervened_answers = self._human_intervention(phase='discussion')
                        if intervened_answers: next_round_answers = intervened_answers
                    # *** END INTERVENTION ***

                    discussion_history.append(next_round_answers)
                    agreement = self.judge.check_agreement(next_round_answers)
                    self.logger.log(f"Judge's Verdict: {'Agreement' if agreement else 'Disagreement'}\n")
                    if agreement:
                        self.logger.log(f"--- Consensus Reached for {text_id} ---\n")
                        break
                
                final_agreements[text_id] = agreement
                discussion_results[text_id] = discussion_history
                final_answers[text_id] = discussion_history[-1]

        return discussion_results, final_answers, final_agreements

    def _run_codebook_evolution_phase(self):
        self.logger.log("********** Codebook Evolution **********\n")
        
        # Initial proposal step
        update_prompt = (
            f"{self.config['prompt']['update']}\n\n"
            f"Here is an example of updating CODEBOOK:\n"
            f"Example ORIGINAL CODEBOOK:\n{self.config['codebook_example']['original']}\n\n"
            f"Example UPDATED CODEBOOK:\n{self.config['codebook_example']['updated']}"
        )
        for agent in self.scientists:
            agent.add_user_message(update_prompt)
        
        self.logger.log("--- Agents Proposing Initial Codebook Updates ---\n")
        proposals = [agent.propose_codebook_update(self.codebook) for agent in self.scientists]
        for i, proposal in enumerate(proposals):
            self.logger.log(f"Agent {i+1}'s Proposal: {proposal}\n")
            
        if self.intervention_enabled and self.intervention_scope == 'extensive':
            intervened = self._human_intervention(phase='codebook proposal')
            if intervened: proposals = intervened
        
        # Multi-round mediation and review loop
        current_proposals = proposals
        final_codebook = ""
        for round_num in range(self.discussion_rounds):
            self.logger.log(f"<Codebook Discussion Round {round_num + 1}>\n")
            
            self.logger.log("--- Mediator Summarizing Proposals ---\n")
            mediator_summary = self.mediator.mediate(current_proposals)
            mediator_message = f"{mediator_summary}\n\nDo you all agree with the unified CODEBOOK?"
            self.logger.log(f"Mediator's Summary & Proposal:\n{mediator_message}\n")
            
            self.logger.log("--- Agents Reviewing Mediated Codebook ---\n")
            opinions = [agent.review_mediated_codebook(mediator_message) for agent in self.scientists]
            for i, opinion in enumerate(opinions):
                self.logger.log(f"Agent {i+1}'s Final Opinion: {opinion}\n")
            
            final_codebook = mediator_summary # Store the latest mediated version

            if self.intervention_enabled and self.intervention_scope == 'extensive':
                intervened_opinions = self._human_intervention(phase=f'codebook review round {round_num+1}')
                if intervened_opinions: opinions = intervened_opinions

            agreement = self.judge.check_agreement(opinions)
            self.logger.log(f"Codebook Agreement Verdict: {'Yes' if agreement else 'No'}\n")
            
            if agreement:
                self.logger.log("--- Consensus on Codebook Reached! ---\n")
                break
            
            current_proposals = opinions # Use latest opinions for the next round
            if round_num == self.discussion_rounds - 1:
                self.logger.log("--- Max rounds reached. Adopting last mediated codebook. ---\n")

        # Update codebook in all scientist agents for the next chunk
        self.codebook = final_codebook
        for agent in self.scientists:
            agent.update_codebook(self.codebook)
        self.logger.log("--- Final Codebook Adopted and Updated for all Agents. ---\n")