from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime


class ImageUploadResponse(BaseModel):
    """Response after image upload"""
    id: int
    filename: str
    upload_method: str
    processing_status: str
    message: str


class URLUploadRequest(BaseModel):
    """Request body for URL-based image upload"""
    url: HttpUrl


class ImageMetadataResponse(BaseModel):
    """Complete image metadata response"""
    id: int
    filename: str
    original_url: Optional[str]
    upload_method: str
    storage_url: Optional[str]
    storage_provider: Optional[str]
    format: str
    width: Optional[int]
    height: Optional[int]
    size_bytes: Optional[int]
    aspect_ratio: Optional[float]
    processing_status: str
    quality_score: Optional[float]
    quality_reasons: Optional[List[str]]
    validation_passed: bool
    validation_errors: Optional[List[str]]
    compliance_passed: Optional[bool]
    compliance_flags: Optional[List[str]]
    is_duplicate: bool
    duplicate_of_id: Optional[int]
    similarity_score: Optional[float]
    cluster_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProcessingResultResponse(BaseModel):
    """Processing result summary"""
    id: int
    processing_status: str
    quality_score: Optional[float]
    quality_reasons: Optional[List[str]]
    validation_passed: bool
    compliance_passed: Optional[bool]
    is_duplicate: bool
    duplicate_of_id: Optional[int]


class ConfigResponse(BaseModel):
    """Configuration and rule thresholds"""
    max_image_size_mb: int
    allowed_formats: List[str]
    min_aspect_ratio: float
    max_aspect_ratio: float
    min_resolution: int
    min_quality_score: float
    min_sharpness_score: float
    min_brightness_score: float
