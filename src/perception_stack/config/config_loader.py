from omegaconf import OmegaConf, DictConfig
from pydantic import ValidationError
from loguru import logger
from perception_stack.config.config_models import RootConfig

def load_and_validate_config(cfg: DictConfig) -> RootConfig:
    """Manual gatekeeper for Hierarchical Configs."""
    # Resolve ${vars} and convert to plain dict
    raw_dict = OmegaConf.to_container(cfg, resolve=True)
    
    try:
        # Instantiate the root hierarchy
        return RootConfig(**raw_dict)
    except ValidationError as e:
        logger.error("❌ Configuration Contract Violated")
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error["loc"])
            logger.error(f"  [{loc}]: {error['msg']}")
        raise