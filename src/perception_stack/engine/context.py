"""
Runtime context builder.

This module defines the BuildContext data model and the factory function
required to initialize it from a validated RootConfig.

Workflow:
    YAML Configs -> RootConfig (Validate) -> BuildContext (Initialize - THIS FILE) -> ...
    -> Registry -> Factory -> Runner -> ...
"""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from perception_stack.config.config_models import RootConfig
from perception_stack.engine.ids import generate_build_id


class ManifestAccumulator(BaseModel):
    """
    Mutable data structure for collecting runtime metrics and metadata.

    This object is intentionally excluded from the frozen state of the
    parent context to allow for incremental updates during pipeline execution.
    """

    total_samples: int = 0
    failed_samples: int = 0
    custom_metadata: dict[str, Any] = Field(default_factory=dict)


class BuildContext(BaseModel):
    """
    Immutable container for dataset build execution state.

    Attributes are populated during instantiation via the create_build_context
    factory function. The model_config setting ensures that all top-level
    fields are read-only after initialization to prevent runtime state drift.
    """

    # Configures the Pydantic model to be immutable
    model_config = ConfigDict(frozen=True)

    # Identifiers and Configuration Reference
    build_id: str
    dataset_name: str
    dataset_version: str | None = None
    config_snapshot: dict[str, Any]

    # Contract and Storage Specifications
    output_namespace: str
    schema_version: str
    ontology_version: str

    # Execution Timing
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Reference to mutable state container
    manifest_accumulator: ManifestAccumulator = Field(default_factory=ManifestAccumulator)

    # Defines a read-only attribute that is dynamically computed from class fields.
    # This allows 'artifact_namespace' to be accessed like a variable (context.artifact_namespace)
    @property
    def artifact_namespace(self) -> str:
        """
        Concatenates storage and identity attributes to form a URI.

        Returns:
            A string representing the authoritative storage path for the build.
        """
        version_part = self.dataset_version or "unversioned"
        base = self.output_namespace.rstrip("/")
        return f"{base}/{self.dataset_name}/{version_part}/{self.build_id}"


def create_build_context(config: RootConfig) -> BuildContext:
    """
    Factory function to map RootConfig values into a BuildContext instance.

    This function extracts validated fields from the RootConfig object and
    generates a unique build_id to initialize the immutable BuildContext.
    """
    return BuildContext(
        build_id=generate_build_id(),
        dataset_name=config.dataset.name,
        dataset_version=config.dataset.version,
        config_snapshot=config.model_dump(mode="json"),
        output_namespace=config.storage.root_path,
        schema_version=config.contract.schema_version,
        ontology_version=config.contract.ontology_version,
    )
