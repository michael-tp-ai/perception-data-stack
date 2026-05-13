"""
-v verbose
-vv extra verbose

Usage:
uv run pytest tests/test_config.py -v

"""

import pytest
from pydantic import ValidationError

from perception_stack.config.config_models import RootConfig


def test_nested_validation_failure() -> None:
    """Ensure errors in the nested 'dataset' model are caught."""
    data = {
        "project_name": "perception_run",
        "dataset": {"name": "test_ds", "version": "1.0"},  # INVALID SEMVER
        "source": {"name": "s", "type": "t"},
        "storage": {"type": "local"},
        "contract": {"schema_version": "v0", "ontology_version": "v0"},
    }
    with pytest.raises(ValidationError) as excinfo:
        RootConfig(**data)

    # Pydantic V2 uses dots for paths in its string representation
    # The output will look like: "dataset.version"
    assert "dataset.version" in str(excinfo.value)


def test_root_strictness() -> None:
    """Ensure extra keys at the root are forbidden."""
    data = {
        "project_name": "test",
        "dataset": {"name": "n", "version": "1.0.0"},
        "source": {"name": "s", "type": "t"},
        "storage": {"type": "local"},
        "random_extra_key": True,
    }
    with pytest.raises(ValidationError):
        RootConfig(**data)
