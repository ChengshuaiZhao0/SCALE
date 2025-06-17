import json
import os
from typing import Dict, Any

def load_config(path: str = './configs/config.json') -> Dict[str, Any]:
    """Loads the configuration file for a given dataset."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file for dataset not found at {path}")

def load_codebook(dataset: str, data_path: str = './data') -> str:
    """Loads the initial codebook for a given dataset."""
    codebook_file = os.path.join(data_path, dataset, 'codebook.txt')
    try:
        with open(codebook_file, 'r', encoding="utf8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Codebook file not found at {codebook_file}")