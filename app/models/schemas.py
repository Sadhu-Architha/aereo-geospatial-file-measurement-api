from typing import Any, Optional
from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    status: str


class FeatureResponse(BaseModel):
    feature_id: int
    geometry_type: str
    geometry: dict[str, Any]
    crs: Optional[str] = None
    properties: dict[str, Any]


class FileDetailsResponse(BaseModel):
    file_id: str
    filename: str
    status: str
    source_crs: Optional[str] = None
    features: list[FeatureResponse]


class MeasurementResponse(BaseModel):
    feature_id: int
    geometry_type: str
    measurement: Optional[float] = None
    unit: Optional[str] = None


class MeasurementsResponse(BaseModel):
    file_id: str
    source_crs: Optional[str] = None
    measurement_crs: Optional[str] = None
    measurements: list[MeasurementResponse]