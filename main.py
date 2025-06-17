import argparse
from utils.config_loader import load_config
from utils.logger import Logger
from simulation.content_analysis_simulation import ContentAnalysisSimulation

def main():
    parser = argparse.ArgumentParser(description="SCALE: Collaborative Content Analysis Simulation")
    parser.add_argument(
        '--path', 
        type=str, 
        default='./configs/config.json', 
        help="Name of the dataset to process (e.g., 'BCD', 'CES')."
    )
    args = parser.parse_args()

    # 1. Load configuration
    config = load_config(args.path)

    # 2. Initialize Logger
    logger = Logger(
        dataset_name=config['dataset_name'],
        model_name=config['settings']['model'],
        seed=config['settings']['seed']
    )
    logger.log(f"Configuration for dataset '{config['dataset_name']}' loaded successfully.\n")

    # 3. Initialize and run the simulation
    simulation = ContentAnalysisSimulation(config, logger)
    simulation.run()

if __name__ == "__main__":
    main()