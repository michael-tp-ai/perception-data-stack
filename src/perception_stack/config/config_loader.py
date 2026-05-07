from typing import Any, Callable
from loguru import logger
from hydra_zen import zen, make_config
from pydantic import ValidationError

from src.config.config_models import DatasetConfig

# We create a Hydra-compatible 'Template' based on our Pydantic Model.
# This tells Hydra what the final dictionary structure should look like.
ConfigSchema = make_config(schema=DatasetConfig)

def validated_task(task_fn: Callable[[DatasetConfig], Any]) -> Callable:
    """
    A professional wrapper that ensures the function 'task_fn' only 
    ever receives a 100% validated DatasetConfig object.
    """
    
    def wrapper(cfg: Any) -> Any:
        try:
            # If hydra-zen has already converted the object, 
            # we ensure it's specifically a DatasetConfig.
            if not isinstance(cfg, DatasetConfig):
                # Manual conversion/validation if called outside hydra-zen
                valid_cfg = DatasetConfig(**cfg)
            else:
                valid_cfg = cfg
                
            return task_fn(valid_cfg)
            
        except ValidationError as e:
            logger.critical("--- CONFIGURATION ERROR ---")
            for error in e.errors():
                loc = " -> ".join(str(x) for x in error["loc"])
                msg = error["msg"]
                logger.error(f"[{loc}]: {msg}")
            
            # Raise SystemExit to stop the pipeline before it starts
            raise SystemExit(1)

    # Use hydra-zen's 'zen' to handle the entry point
    return zen(wrapper)