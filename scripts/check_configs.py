# """
# Acts as a "Dry Run" linter. 
# It simulates Hydra composition and Pydantic validation to ensure YAML files match the project's data contract without 
# initializing the full perception engine.

# Usage
# uv run python scripts/check_config.py

# ######
# PROPOSED EVENTUAL INTEGRATION
# Integration Strategy
# 1. CI/CD Gatekeeper
# Context: GitHub Actions / GitLab CI.
# Role: Automatically runs on every Pull Request.
# Impact: Blocks merging if configurations are structurally invalid (typos, missing fields, SemVer violations).

# 2. Production Pre-Flight
# Context: Docker Entrypoint / Kubernetes Pod.
# Role: Runs as the first command in the startup sequence.
# Impact: Prevents allocating expensive GPU or simulation resources (Isaac Sim) if the runtime configuration is destined to fail.
# """
import os
import sys

from hydra import compose, initialize_config_dir
from loguru import logger
from rich.console import Console
from rich.panel import Panel

from perception_stack.config.config_loader import load_and_validate_config

console = Console()

def run_check():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "configs")
    
    try:
        with initialize_config_dir(version_base="1.3", config_dir=config_path):
            raw_cfg = compose(config_name="config")
            
            # The return value is our RootConfig object
            validated_cfg = load_and_validate_config(raw_cfg)
            logger.success(f"✅ Project '{validated_cfg.project_name}' [Dataset: {validated_cfg.dataset.name}] is valid.")
            
            # --- INSPECTION BLOCK ---
            console.print("\n[bold cyan]Validated RootConfig Inspection:[/bold cyan]")
            
            # model_dump_json() creates an indented view of the data
            json_data = validated_cfg.model_dump_json(indent=2)
            console.print(Panel(json_data, title="Final Validated Intent", expand=False))
            
            # You can also access fields directly via dot notation
            console.print(f"[green]✔[/green] Project: [bold]{validated_cfg.project_name}[/bold]")
            console.print(f"[green]✔[/green] Source Type: [yellow]{validated_cfg.source.type}[/yellow]")
            # ------------------------
            
    except Exception as e:
        logger.critical(f"🛑 Configuration check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_check()