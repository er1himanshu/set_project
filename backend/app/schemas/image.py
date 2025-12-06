from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class ImageCreate(BaseModel):
    """Schema for creating an image via URL."""
    url: HttpUrl


class ImageUploadResponse(BaseModel):
    """Response after uploading an image."""
    id: int
    filename: str
    status: str
    message: str = "Image uploaded successfully and queued for processing"


class ProcessingResult(BaseModel):
    """Detailed processing results for an image."""
    quality_score: Optional[float] = None
    quality_reasons: Optional[List[str]] = None
    is_compliant: Optional[bool] = None
    compliance_flags: Optional[List[str]] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[int] = None
    cluster_id: Optional[str] = None


class ImageResponse(BaseModel):
    """Full image metadata and results."""
    id: int
    filename: str
    original_url: Optional[str] = None
    storage_path: Optional[str] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    status: str
    quality_score: Optional[float] = None
    quality_reasons: Optional[List[str]] = None
    is_compliant: Optional[bool] = None
    compliance_flags: Optional[List[str]] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[int] = None
    cluster_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class ConfigResponse(BaseModel):
    """Configuration thresholds for display."""
    max_file_size_mb: int
    min_width: int
    min_height: int
    max_width: int
    max_height: int
    allowed_formats: List[str]
    min_quality_score: float
    min_resolution_threshold: int
    max_compression_artifacts: float
