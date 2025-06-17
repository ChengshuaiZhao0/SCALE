import json
import os
from datetime import datetime
from typing import Dict, Any, List

class Logger:
    """Handles logging of the simulation process to console and files."""
    def __init__(self, dataset_name: str, model_name: str, seed: int):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_dir = os.path.join('results', model_name, f'{timestamp}_{dataset_name}_{seed}')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file_path = os.path.join(self.log_dir, 'log.txt')
        self.log_data = []

    def log(self, message: str, to_console: bool = True):
        """Logs a message to the console and the log file."""
        if to_console:
            print(message)
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
            f.flush()

    def save_json(self, data: Any, filename: str):
        """Saves data to a JSON file in the log directory."""
        path = os.path.join(self.log_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)