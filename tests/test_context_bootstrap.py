"""
Integration tests for the BuildContext.

This module verifies that the BuildContext can be successfully constructed
using the real YAML configuration files located in the /configs directory.
"""

import pytest
from hydra import compose, initialize
from pydantic import ValidationError

from perception_stack.config.config_models import RootConfig
from perception_stack.engine import create_build_context


def test_full_engine_chain_integration() -> None:
    """
    Tests the mapping of YAML values into a frozen BuildContext object.

    This ensures that the RootConfig bouncer and the BuildContext factory
    correctly handle real-world configuration data.
    """
    # Initialize Hydra from the actual configs directory
    with initialize(version_base=None, config_path="../configs"):
        cfg = compose(config_name="config", overrides=[])

    # 1. Verify Configuration Validation
    root_cfg = RootConfig(**dict(cfg))  # casts the Hydra obj to a standard Python dict

    # 2. Verify Context Initialization
    context = create_build_context(root_cfg)

    # 3. Assert Identity and Metadata
    assert context.build_id.startswith("build_")
    assert context.dataset_name == "demo"
    assert context.dataset_version == "0.1.0"
    assert context.schema_version == "v0"

    # 4. Verify Computed Artifact Namespace
    assert context.build_id in context.artifact_namespace
    assert context.dataset_name in context.artifact_namespace
    assert context.dataset_version in context.artifact_namespace

    # 5. Verify Timing (Matching the 'start_time' field in context.py)
    assert context.start_time is not None
    assert context.start_time.tzinfo is not None

    # 6. Verify Immutability (Lamination check)
    with pytest.raises(ValidationError):
        # We use a clean ignore. If Mypy says it is unused, we add the second ignore
        # to handle the 'unused-ignore' error itself.
        context.dataset_name = "malicious_update_attempt"  # type: ignore[misc, unused-ignore]
