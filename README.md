# SCALE: Towards Collaborative Content Analysis in Social Science with Large Language Model Agents and Human Intervention

[![Paper](https://img.shields.io/badge/Paper-arXiv:2502.10937-#40d9b0ff.svg)](https://arxiv.org/abs/2502.10937)

This repository contains the official Python implementation of the framework described in the paper **"SCALE: Towards Collaborative Content Analysis in Social Science with Large Language Model Agents and Human Intervention"**, accepted at ACL 2025.

## News
- **[07/13/2025]** A presentation video is available on [YouTube](https://youtu.be/Fq7cutzHdOM).
- **[06/16/2025]** An example implementation of the SCALE framework is now available!
- **[05/16/2025]** GitHub repository created. Code release is coming soon.
- **[05/15/2025]** Our paper has been accepted by the main conference of **ACL 2025**. 🚀
- **[02/16/2025]** Our paper is available on [arXiv](https://arxiv.org/abs/2502.10937).

## Introduction

Content analysis is a foundational research method in the social sciences for breaking down unstructured text into structured, theory-informed categories. This process is often manual, labor-intensive, and time-consuming.

To address these challenges, we introduce **SCALE**, a novel multi-agent framework that effectively **S**imulates **C**ollaborative **A**nalysis via **L**arge language model ag**E**nts. By harnessing LLM agents with distinct personas and incorporating various modes of human intervention, SCALE automates the content analysis workflow to produce reliable, high-quality annotations at scale.

![SCALE](figure/main.png)
## The SCALE Workflow

The SCALE framework mirrors the process of real-world content analysis through four primary steps, which form an iterative cycle for analysis and refinement.

1.  **Coder Simulation**
    The process begins by configuring multiple LLM agents, each emulating a seasoned social scientist with a distinct, real-world-based persona. An initial codebook is also established, which can either be predefined by human experts or created from scratch by the agents.

2.  **Bot Annotation**
    Each agent autonomously annotates an identical batch of text entries. In this phase, agents work independently, strictly following the guidelines in the current codebook to classify each text into a discrete category.

3.  **Agent Discussion**
    When disagreements in annotations arise, the agents initiate a structured, multi-round discussion to resolve their differences. They exchange reasoning and update their annotations based on peer feedback until they converge on a unanimous decision.

4.  **Codebook Evolution**
    In the final phase of the cycle, agents collaboratively refine and update the codebook based on insights gained from their discussions. This can involve enriching rules with new examples or modifying the categories themselves. This newly refined codebook is then used for the next cycle of annotation, ensuring continuous improvement.

## Key Features

-   **Multi-Agent Simulation**: Deploys multiple LLM agents, each with a unique, configurable persona to foster diverse perspectives and robust discussions.
-   **Praxis-Informed Design**: The workflow is developed in close collaboration with social scientists, ensuring it faithfully reflects the principles and standards of manual content analysis.
-   **Human Intervention**: Provides a flexible portal for human experts to intervene in the. The intervention can be configured by both scope and role:
    -   **Scope**: targeted (discussion phase only) or extensive (discussion and codebook evolution phases).
    -   **Authority**: collaborative (agents may accept or reject advice) or directive (agents must follow instructions).
-   **Highly Configurable**: The entire simulation—including agent personas, prompts, datasets, and intervention strategies—is controlled via easy-to-edit JSON configuration files.
-   **Modular & Extensible**: Built with a clean, object-oriented architecture that separates agents, simulation logic, and utilities, making the code easy to understand and extend.

## Project Structure

The project is organized into a modular structure for clarity and maintainability:

```
scale-project/
├── main.py                   # Main entry point to run the simulation
├── requirements.txt          # Python dependencies
├── configs/                  # Directory for JSON configuration files
│   └── config.json
├── data/                     # Directory for datasets
│   └── EXP/                  # An Example dataset
│       ├── data.xlsx         # The text data for analysis
│       └── codebook.txt      # The initial codebook
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

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/ChengshuaiZhao0/SCALE.git
    ```

2.  **Create a Conda Environment (Recommended)**

    ```bash
    conda create -n scale python=3.12
    conda activate scale
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The simulation is controlled by a JSON file located in the `configs/` directory (e.g., `configs/config.json`).

#### Configuration Options:

-   `api_key`: Add your OpenAI API key here.
-   `dataset_name`: The name of the dataset, which must match the folder name in `data/`.
-   `settings`:
    -   `agents`: The number of social scientist agents to simulate.
    -   `rounds`: The maximum number of discussion rounds.
    -   `chunk_size`: The number of text entries to process in each cycle.
    -   `model`: The OpenAI model to use (e.g., `gpt-4o-mini`).
    -   `intervention`:
        -   `enabled`: Set to `true` to allow human intervention.
        -   `scope`: `targeted` or `extensive`.
        -   `authority`: `collaborative` or `directive`.
-   `persona`: Define the background and personality for each agent.
-   `prompt`: Contains the text for all prompts used by SCALE framework.
-   `codebook_example`: Provides an in-context learning example of an `original` and `updated` codebook to guide the agents during the evolution phase.

#### Data Preparation:

Due to the sensitive nature of the datasets used in this research, they are not publicly available for direct download. We are committed to upholding ethical standards for data privacy. Researchers interested in obtaining the datasets for academic and non-commercial purposes can request access by filling out the following form. Upon approval, you will receive instructions on how to access the data.

**➡️ [Data Request Form](https://forms.gle/eUnAihddtooCePgW9)**

*After submitting the form, we recommend contacting ezhao[at]unc.edu and czhao93[at]asu.edu to follow up on your request.*

Once you have received the data files:

-   Place your dataset as an `.xlsx` file inside a corresponding folder in `data/` (e.g., `data/CN-NES/data.xlsx`).
-   The Excel file must contain a column named `Text` with the content to be analyzed.
-   Place the initial codebook in a file named `codebook.txt` within the same folder.

> For reference and quick setup, we also provide **an example codebook and dataset** (not used in the paper) in the `data/EXP` directory.

## How to Run

To run the simulation, execute the `main.py` script from the root directory.

```bash
python main.py
```

-   All output, including detailed logs and final results, will be saved to a timestamped folder within the `results/` directory.
-   If intervention is enabled in the config, the program will prompt you for input in the terminal at the appropriate steps.

## Citation

If you found this repo useful, please feel free to cite our work!

```bibtex
@article{zhao2025scale,
  title={Scale: Towards collaborative content analysis in social science with large language model agents and human intervention},
  author={Zhao, Chengshuai and Tan, Zhen and Wong, Chau-Wai and Zhao, Xinyan and Chen, Tianlong and Liu, Huan},
  journal={arXiv preprint arXiv:2502.10937},
  year={2025}
}
```
