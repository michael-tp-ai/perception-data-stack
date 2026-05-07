import os
import sys
from hydra import initialize_config_dir, compose
from loguru import logger
from perception_stack.config.config_loader import load_and_validate_config

def run_check():
    # Absolute path to /configs
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "configs")
    
    try:
        with initialize_config_dir(version_base="1.3", config_dir=config_path):
            # Compose merges configs/dataset/demo.yaml into the 'dataset' key
            raw_cfg = compose(config_name="config")
            
            validated_cfg = load_and_validate_config(raw_cfg)
            logger.success(f"✅ Project '{validated_cfg.project_name}' [Dataset: {validated_cfg.dataset.name}] is valid.")
            
    except Exception:
        logger.critical("🛑 Configuration check failed.")
        sys.exit(1)

if __name__ == "__main__":
    run_check()