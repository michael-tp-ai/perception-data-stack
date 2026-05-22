from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    POINT_CLOUD = "point_cloud"


class Modality(str, Enum):
    RGB = "rgb"
    DEPTH = "depth"
    INFRARED = "infrared"
    LIDAR = "lidar"


class ValidationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    UNVERIFIED = "unverified"


class OntologyClass(BaseModel):
    """Defines an allowed semantic class within the dataset ontology."""

    class_id: str = Field(..., description="Unique machine-readable name, e.g., 'vehicle.car'")
    display_name: str
    description: str | None = None


class BoundingBox2D(BaseModel):
    """Normalized 2D bounding box coordinates in [0.0, 1.0]."""

    xmin: float = Field(..., ge=0.0, le=1.0)
    ymin: float = Field(..., ge=0.0, le=1.0)
    xmax: float = Field(..., ge=0.0, le=1.0)
    ymax: float = Field(..., ge=0.0, le=1.0)

    @field_validator("xmax")
    @classmethod
    def validate_x_bounds(cls, value: float, info: Any) -> float:
        if "xmin" in info.data and value <= info.data["xmin"]:
            raise ValueError("xmax must be greater than xmin")
        return value

    @field_validator("ymax")
    @classmethod
    def validate_y_bounds(cls, value: float, info: Any) -> float:
        if "ymin" in info.data and value <= info.data["ymin"]:
            raise ValueError("ymax must be greater than ymin")
        return value


class ObjectAnnotation(BaseModel):
    """Represents a single labeled object instance inside a media sample."""

    annotation_id: str
    class_id: str
    geometry: BoundingBox2D
    attributes: dict[str, Any] = Field(default_factory=dict)


class MediaReference(BaseModel):
    """Pointer and metadata for a physical media asset."""

    uri: str = Field(..., description="Remote URI or local path")
    media_type: MediaType
    modality: Modality = Modality.RGB
    checksum: str | None = Field(None, description="Optional asset checksum")
    width: int | None = Field(None, gt=0)
    height: int | None = Field(None, gt=0)
    frame_count: int | None = Field(None, gt=0)


class Provenance(BaseModel):
    """Traceability fields describing where this sample came from."""

    source_type: str
    source_name: str
    source_record_id: str
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_component: str
    source_component_version: str | None = None


class QualityMetrics(BaseModel):
    """Runtime quality and validation information."""

    validation_status: ValidationStatus = ValidationStatus.UNVERIFIED
    blurriness_score: float | None = Field(None, ge=0.0, le=1.0)
    exposure_score: float | None = Field(None, ge=0.0, le=1.0)
    validation_errors: list[str] = Field(default_factory=list)


class CanonicalSample(BaseModel):
    """Standard internal representation for one dataset sample."""

    schema_version: str = "v0"
    sample_id: str
    dataset_name: str
    media: MediaReference
    annotations: list[ObjectAnnotation] = Field(default_factory=list)
    provenance: Provenance
    quality: QualityMetrics = Field(default_factory=QualityMetrics)
    custom_metadata: dict[str, Any] = Field(default_factory=dict)
