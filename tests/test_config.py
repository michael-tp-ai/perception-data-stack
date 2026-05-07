import pytest
from pydantic import ValidationError
from src.perception_stack.config.config_models import RootConfig

def test_nested_validation_failure():
    """Ensure errors in the nested 'dataset' model are caught."""
    data = {
        "project_name": "perception_run",
        "dataset": {"name": "test_ds", "version": "1.0"}, # INVALID SEMVER
        "source": {"name": "s", "type": "t"},
        "storage": {"type": "local"}
    }
    with pytest.raises(ValidationError) as excinfo:
        RootConfig(**data)
    
    # Verify the error path points correctly into the nested model
    assert "dataset -> version" in str(excinfo.value)

def test_root_strictness():
    """Ensure extra keys at the root are forbidden."""
    data = {
        "project_name": "test",
        "dataset": {"name": "n", "version": "1.0.0"},
        "source": {"name": "s", "type": "t"},
        "storage": {"type": "local"},
        "random_extra_key": True 
    }
    with pytest.raises(ValidationError):
        RootConfig(**data)