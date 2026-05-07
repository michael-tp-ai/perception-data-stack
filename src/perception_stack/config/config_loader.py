from typing import Any, cast

from loguru import logger
from omegaconf import DictConfig, OmegaConf
from pydantic import ValidationError

from perception_stack.config.config_models import RootConfig


def load_and_validate_config(cfg: DictConfig) -> RootConfig:
    """Manual gatekeeper for Hierarchical Configs."""
    ### Resolve ${vars} and convert to plain dict
    ### raw_dict = OmegaConf.to_container(cfg, resolve=True)

    # 1. We cast the result to dict[str, Any] so Mypy knows it's a mapping
    raw_dict = cast(dict[str, Any], OmegaConf.to_container(cfg, resolve=True))

    # 2. Safety check: In case Hydra somehow returns None or something else
    if not isinstance(raw_dict, dict):
        raise ValueError(f"Expected configuration to be a mapping, got {type(raw_dict)}")

    try:
        # Instantiate the root hierarchy
        return RootConfig(**raw_dict)
    except ValidationError as e:
        logger.error("❌ Configuration Contract Violated")
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error["loc"])
            logger.error(f"  [{loc}]: {error['msg']}")
        raise
