from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class ComponentConfig(BaseModel):
    """Base schema for modular components (Sources, Annotators, etc.)"""
    model_config = ConfigDict(extra="forbid") # Prevents unrecognized keys
    
    type: str = Field(..., description="The registry key for the component implementation")
    enabled: bool = Field(default=True, description="Whether to execute this component")
    params: Dict[str, Any] = Field(default_factory=dict, description="Component-specific arguments")

class SourceConfig(ComponentConfig):
    """Specific configuration for data ingestion"""
    name: str = Field(..., description="Logical name of the data source")

class StorageConfig(ComponentConfig):
    """Specific configuration for data persistence"""
    root_path: str = Field(default="artifacts/datasets", description="Base directory for outputs")

class DatasetConfig(BaseModel):
    """ The Root Configuration Object for a Dataset Build """
    model_config = ConfigDict(extra="forbid")

    project_name: str = Field(..., min_length=1)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$") # Enforces SemVer (e.g. 1.0.2)
    
    # Core Pipeline Steps
    source: SourceConfig
    storage: StorageConfig
    
    # Modular Components
    annotators: List[ComponentConfig] = Field(default_factory=list)
    hooks: List[ComponentConfig] = Field(default_factory=list)
    
    # Optional metadata
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)