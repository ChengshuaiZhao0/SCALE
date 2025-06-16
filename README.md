# SCALE: Towards Collaborative Content Analysis in Social Science with Large Language Model Agents and Human Intervention

[![Paper](https://img.shields.io/badge/Paper-ArXiv-green)](https://arxiv.org/pdf/2502.10937)

## News

- [6/16/2025] We upload an exmple implementation of SCALE!
- [5/16/2025] We create this Github repo. The code will be available very soon!
- [5/15/2025] Our paper has been accepted by at **ACL 2025** main conference. 🚀
- [2/16/2025] We upload [paper](https://arxiv.org/pdf/2502.10937) to ArXiv.

## Intro

This repository contains the Python implementation of the framework described in the paper: **"SCALE: Towards Collaborative Content Analysis in Social Science with Large Language Model Agents and Human Intervention"**.

SCALE is a novel multi-agent framework that effectively **<u>S</u>**imulates **<u>C</u>**ollaborative <u>**A**</u>nalysis via <u>**L**</u>arge language model ag***E***nts. It is designed to automate the rigorous and labor-intensive process of content analysis, a critical research method in the social sciences. The system mimics key phases of manual content analysis, including independent text coding, collaborative discussion to resolve discrepancies, and dynamic evolution of the coding rules (the "codebook").

By harnessing LLM agents with distinct personas and incorporating various modes of human intervention, SCALE aims to achieve human-approximated performance, reduce subjectivity, and enable high-quality, large-scale textual analysis.

## Features

- **Multi-Agent Simulation**: Deploys multiple LLM agents, each with a unique persona derived from real-world social scientists, to foster diverse perspectives and robust discussions.
- **Dynamic Three-Phase Workflow**: Faithfully simulates the core workflow of traditional content analysis:
  1. Bot Annotation: Agents independently annotate text based on a shared codebook.
  2. Agent Discussion: Agents engage in multi-round discussions to resolve inconsistencies in their annotations.
  3. Codebook Evolution: Agents collaboratively refine and update the codebook based on insights gained from their discussions, which is then used in subsequent cycles.
- **Human-intervention**: Provides a flexible portal for human experts to intervene in the process. The intervention can be configured by scope and role:
  - Scope: `targeted` (discussion phase only) or `extensive` (discussion and codebook evolution phase).
  - Authority: `collaborative` (agents can accept or reject advice) or `directive` (agents must follow instructions).
- **Highly Configurable**: The entire simulation—including agent personas, prompts, datasets, and intervention strategies—is controlled via easy-to-edit JSON configuration files.
- **Modular & Extensible**: Built with a clean, object-oriented architecture that separates agents, simulation logic, and utilities, making the code easy to understand, maintain, and extend for future research.

## Project Structure

The project is organized into a modular structure for clarity and maintainability:

```
scale-project/
├── main.py                   # Main entry point to run the simulation
├── requirements.txt          # Python dependencies
├── configs/                  # Directory for JSON configuration files
│   └── CES.json
├── data/                     # Directory for datasets
│   └── CES/
│       ├── data.xlsx         # The text data for analysis
│       └── original_rules.txt# The initial codebook
├── results/                  # Output directory for logs and results
├── agents/                   # Contains all agent class definitions
│   ├── base_agent.py
│   ├── social_scientist_agent.py
│   ├── judge_agent.py
│   ├── mediator_agent.py
│   └── human_expert.py
├── simulation/               # The core simulation orchestrator
│   └── content_analysis_simulation.py
└── utils/                    # Helper utilities
    ├── config_loader.py
    └── logger.py
```

## Setup and Installation

1. **Clone the Repository**

   ```Bash
   git clone https://github.com/ChengshuaiZhao0/SCALE.git
   cd SCALE
   ```

2. **Create a Virtual Environment (Recommended)**

   ```Bash
   conda create -n scale python==3.12
   conda activate scale
   ```

3. **Install Dependencies** Install all required Python packages using the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The simulation is controlled by a JSON file located in the `configs/` directory. You can create new configuration files for different datasets or experiments.

### Key Configuration Options (`configs/config.json`):

- `api_key`: You must add your OpenAI API key here.
- `dataset_name`: The name of the dataset, which should match the folder name in `data/`.
- `settings`:
  - `agents`: The number of social scientist agents to simulate.
  - `rounds`: The maximum number of discussion rounds for both text annotation and codebook evolution.
  - `chunk_size`: The number of text entries to process in each full cycle.
  - `model`: The OpenAI model to use (e.g., `gpt-4o-mini`).
  - `intervention`:
    - `enabled`: Set to `true` to allow human intervention.
    - `scope`: `targeted` or `extensive`.
    - `authority`: `collaborative` or `directive`.
- `persona`: Define the background and personality for each agent. The system will cycle through these personas if `agents` > number of personas.
- `prompt`: Contains the text for all system prompts used by the agents (`coding`, `discussion`, `judge`, `mediator`, `collaborative`, `directive`, etc.).
- `codebook_example`: Provides an example of an `original` and `updated` codebook to guide the agents during the evolution phase.

### Data Preparation:

- Place your dataset as an `.xlsx` file inside a folder in `data/` (e.g., `data/CES/data.xlsx`).
- The dataset file should contain a column with the Text to be analyzed.
- Place the initial codebook in a file named `original_rules.txt` within the same folder.

## How to Run

To run the simulation, execute the `main.py` script from the root directory, specifying the dataset you wish to process.

```bash
python main.py
```

- All output, including detailed logs and final results, will be saved to a timestamped folder within the `results/` directory.
- If intervention is enabled, the program will prompt for your input in the terminal at the appropriate points in the simulation.

## Citation

If you found it useful, please feel free to  cite our work:

```tex
@article{zhao2025scale,
  title={Scale: Towards collaborative content analysis in social science with large language model agents and human intervention},
  author={Zhao, Chengshuai and Tan, Zhen and Wong, Chau-Wai and Zhao, Xinyan and Chen, Tianlong and Liu, Huan},
  journal={arXiv preprint arXiv:2502.10937},
  year={2025}
}
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
