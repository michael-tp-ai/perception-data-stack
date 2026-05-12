"""
This module defines the strict Pydantic schemas used to validate the raw
YAML configurations loaded by Hydra. It acts as the pipeline's "gatekeeper,"
ensuring all required fields, types, and contracts are correct before execution.

The resulting `RootConfig` object serves as the single, strongly-typed source
of truth used to initialize the engine's BuildContext and ComponentFactory.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ComponentConfig(BaseModel):
    """Base for pluggable modules."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    type: str = Field(..., description="Registry key for implementation")
    enabled: bool = True
    params: dict[str, Any] = Field(default_factory=dict)


class SourceConfig(ComponentConfig):
    """Data ingestion component metadata"""

    name: str = Field(..., min_length=1)  # min_length=1 enforces a non-empty string
    path: str | None = None


class StorageConfig(ComponentConfig):
    """Intent for data persistence."""

    root_path: str = "artifacts/datasets"


class DatasetConfig(BaseModel):
    """Describes the core data of the output."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    description: str | None = None


class ContractConfig(BaseModel):
    """Defines the expected canonical data formats."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    schema_version: str = Field(..., min_length=1)
    ontology_version: str = Field(..., min_length=1)


class RootConfig(BaseModel):
    """Aggregates all of the above info into a final RootConfig object"""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    project_name: str = Field(..., min_length=1)
    dataset: DatasetConfig
    source: SourceConfig
    contract: ContractConfig
    storage: StorageConfig

    annotators: list[ComponentConfig] = Field(default_factory=list)
    hooks: list[ComponentConfig] = Field(default_factory=list)
