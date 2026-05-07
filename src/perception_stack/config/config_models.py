from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ComponentConfig(BaseModel):
    """Machinery: Base for pluggable modules."""
    model_config = ConfigDict(extra="forbid", validate_default=True)
    
    type: str = Field(..., description="Registry key for implementation")
    enabled: bool = True
    params: dict[str, Any] = Field(default_factory=dict)

class SourceConfig(ComponentConfig):
    """Machinery: Intent for data ingestion."""
    name: str = Field(..., min_length=1)
    path: str | None = None

class StorageConfig(ComponentConfig):
    """Machinery: Intent for data persistence."""
    root_path: str = "artifacts/datasets"

class DatasetConfig(BaseModel):
    """Metadata: Describes the 'What' of the output."""
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(..., min_length=1)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    description: str | None = None

class RootConfig(BaseModel):
    """The Root: Aggregates Identity, Metadata, and Machinery."""
    model_config = ConfigDict(extra="forbid", validate_default=True)

    project_name: str = Field(..., min_length=1)
    dataset: DatasetConfig
    source: SourceConfig
    storage: StorageConfig
    
    annotators: list[ComponentConfig] = Field(default_factory=list)
    hooks: list[ComponentConfig] = Field(default_factory=list)