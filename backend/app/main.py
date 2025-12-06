from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import httpx
from typing import List

from app.config import settings
from app.database import get_db, init_db
from app.models import ImageMetadata
from app.schemas import (
    ImageUploadResponse,
    URLUploadRequest,
    ImageMetadataResponse,
    ProcessingResultResponse,
    ConfigResponse
)
from app.validators import validate_image
from app.tasks import process_image
from app.url_validator import is_safe_url

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Image Quality Analysis and Management System for E-commerce",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
# TODO: In production, restrict allow_origins to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Image Quality Analysis System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/images/upload/file", response_model=ImageUploadResponse)
async def upload_image_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an image file for processing.
    
    The image will be validated and queued for asynchronous processing
    (quality analysis, compliance check, duplicate detection).
    """
    # Read file content
    image_bytes = await file.read()
    
    # Validate image
    image, metadata, validation_errors = validate_image(image_bytes, file.filename)
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": validation_errors}
        )
    
    # Create database record
    image_record = ImageMetadata(
        filename=file.filename,
        upload_method="file",
        format=metadata["format"],
        width=metadata["width"],
        height=metadata["height"],
        size_bytes=metadata["size_bytes"],
        aspect_ratio=metadata["aspect_ratio"],
        validation_passed=len(validation_errors) == 0,
        validation_errors=validation_errors if validation_errors else None,
        processing_status="pending"
    )
    
    db.add(image_record)
    db.commit()
    db.refresh(image_record)
    
    # Queue processing task
    process_image.delay(image_record.id)
    
    return ImageUploadResponse(
        id=image_record.id,
        filename=file.filename,
        upload_method="file",
        processing_status="pending",
        message="Image uploaded successfully and queued for processing"
    )


@app.post("/api/images/upload/url", response_model=ImageUploadResponse)
async def upload_image_url(
    request: URLUploadRequest,
    db: Session = Depends(get_db)
):
    """
    Upload an image from a URL for processing.
    
    The image will be downloaded, validated, and queued for asynchronous processing.
    """
    # Validate URL to prevent SSRF attacks
    url_str = str(request.url)
    is_safe, error_msg = is_safe_url(url_str)
    
    if not is_safe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": [error_msg]}
        )
    
    # Download image from URL
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url_str, timeout=30.0, follow_redirects=False)
            response.raise_for_status()
            image_bytes = response.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": [f"Failed to download image: {str(e)}"]}
        )
    
    # Extract filename from URL
    filename = str(request.url).split("/")[-1].split("?")[0] or "image.jpg"
    
    # Validate image
    image, metadata, validation_errors = validate_image(image_bytes, filename)
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": validation_errors}
        )
    
    # Create database record
    image_record = ImageMetadata(
        filename=filename,
        original_url=str(request.url),
        upload_method="url",
        format=metadata["format"],
        width=metadata["width"],
        height=metadata["height"],
        size_bytes=metadata["size_bytes"],
        aspect_ratio=metadata["aspect_ratio"],
        validation_passed=len(validation_errors) == 0,
        validation_errors=validation_errors if validation_errors else None,
        processing_status="pending"
    )
    
    db.add(image_record)
    db.commit()
    db.refresh(image_record)
    
    # Queue processing task
    process_image.delay(image_record.id)
    
    return ImageUploadResponse(
        id=image_record.id,
        filename=filename,
        upload_method="url",
        processing_status="pending",
        message="Image downloaded and queued for processing"
    )


@app.get("/api/images", response_model=List[ImageMetadataResponse])
async def list_images(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all processed images with metadata and results.
    """
    images = db.query(ImageMetadata)\
        .order_by(ImageMetadata.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return images


@app.get("/api/images/{image_id}", response_model=ImageMetadataResponse)
async def get_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific image.
    """
    image = db.query(ImageMetadata).filter(ImageMetadata.id == image_id).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return image


@app.get("/api/images/{image_id}/result", response_model=ProcessingResultResponse)
async def get_processing_result(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Get processing result summary for an image.
    """
    image = db.query(ImageMetadata).filter(ImageMetadata.id == image_id).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return ProcessingResultResponse(
        id=image.id,
        processing_status=image.processing_status,
        quality_score=image.quality_score,
        quality_reasons=image.quality_reasons,
        validation_passed=image.validation_passed,
        compliance_passed=image.compliance_passed,
        is_duplicate=image.is_duplicate,
        duplicate_of_id=image.duplicate_of_id
    )


@app.get("/api/config", response_model=ConfigResponse)
async def get_config():
    """
    Get current configuration and rule thresholds.
    """
    return ConfigResponse(
        max_image_size_mb=settings.MAX_IMAGE_SIZE_MB,
        allowed_formats=settings.allowed_formats_list,
        min_aspect_ratio=settings.MIN_ASPECT_RATIO,
        max_aspect_ratio=settings.MAX_ASPECT_RATIO,
        min_resolution=settings.MIN_RESOLUTION,
        min_quality_score=settings.MIN_QUALITY_SCORE,
        min_sharpness_score=settings.MIN_SHARPNESS_SCORE,
        min_brightness_score=settings.MIN_BRIGHTNESS_SCORE
    )


@app.delete("/api/images/{image_id}")
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an image record.
    """
    image = db.query(ImageMetadata).filter(ImageMetadata.id == image_id).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    db.delete(image)
    db.commit()
    
    return {"message": "Image deleted successfully"}
