import os
import uuid
import httpx
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from PIL import Image as PILImage

from app.core.database import get_db
from app.core.config import settings
from app.models.image import Image
from app.schemas.image import (
    ImageCreate,
    ImageResponse,
    ImageUploadResponse,
    ConfigResponse
)
from app.services.validation import ImageValidator, ValidationError
from app.services.storage import StorageService
from app.tasks.image_processing import process_image

router = APIRouter()


@router.post("/upload/file", response_model=ImageUploadResponse)
async def upload_image_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an image file for processing.
    Validates the image and enqueues a processing job.
    """
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    temp_path = f"/tmp/{unique_filename}"
    
    try:
        # Save uploaded file temporarily
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Get file size
        file_size = len(content)
        
        # Open and validate image
        img = PILImage.open(temp_path)
        validator = ImageValidator()
        
        try:
            validator.validate_image(img, file_size)
        except ValidationError as e:
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail=str(e))
        
        # Save to configured storage
        storage_path = StorageService.save_image(temp_path, unique_filename)
        
        # Create database record
        image_record = Image(
            filename=unique_filename,
            original_url=None,
            storage_path=storage_path,
            file_size=file_size,
            width=img.width,
            height=img.height,
            format=img.format,
            status="pending"
        )
        db.add(image_record)
        db.commit()
        db.refresh(image_record)
        
        # Enqueue processing job
        process_image.delay(image_record.id)
        
        # Clean up temp file if different from storage
        if temp_path != storage_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return ImageUploadResponse(
            id=image_record.id,
            filename=image_record.filename,
            status=image_record.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/upload/url", response_model=ImageUploadResponse)
async def upload_image_url(
    image_data: ImageCreate,
    db: Session = Depends(get_db)
):
    """
    Upload an image from URL for processing.
    Downloads, validates, and enqueues a processing job.
    """
    url = str(image_data.url)
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.jpg"
    temp_path = f"/tmp/{unique_filename}"
    
    try:
        # Download image
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            with open(temp_path, "wb") as f:
                f.write(response.content)
        
        file_size = len(response.content)
        
        # Open and validate image
        img = PILImage.open(temp_path)
        validator = ImageValidator()
        
        try:
            validator.validate_image(img, file_size)
        except ValidationError as e:
            os.remove(temp_path)
            raise HTTPException(status_code=400, detail=str(e))
        
        # Save to configured storage
        storage_path = StorageService.save_image(temp_path, unique_filename)
        
        # Create database record
        image_record = Image(
            filename=unique_filename,
            original_url=url,
            storage_path=storage_path,
            file_size=file_size,
            width=img.width,
            height=img.height,
            format=img.format,
            status="pending"
        )
        db.add(image_record)
        db.commit()
        db.refresh(image_record)
        
        # Enqueue processing job
        process_image.delay(image_record.id)
        
        # Clean up temp file if different from storage
        if temp_path != storage_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return ImageUploadResponse(
            id=image_record.id,
            filename=image_record.filename,
            status=image_record.status
        )
        
    except HTTPException:
        raise
    except httpx.HTTPError as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/images", response_model=List[ImageResponse])
def list_images(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all images with their processing results.
    """
    images = db.query(Image).order_by(Image.created_at.desc()).offset(skip).limit(limit).all()
    return images


@router.get("/images/{image_id}", response_model=ImageResponse)
def get_image(
    image_id: int,
    db: Session = Depends(get_db)
):
    """
    Get details for a specific image.
    """
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.get("/config", response_model=ConfigResponse)
def get_config():
    """
    Get current configuration thresholds.
    """
    return ConfigResponse(
        max_file_size_mb=settings.MAX_FILE_SIZE_MB,
        min_width=settings.MIN_WIDTH,
        min_height=settings.MIN_HEIGHT,
        max_width=settings.MAX_WIDTH,
        max_height=settings.MAX_HEIGHT,
        allowed_formats=settings.ALLOWED_FORMATS,
        min_quality_score=settings.MIN_QUALITY_SCORE,
        min_resolution_threshold=settings.MIN_RESOLUTION_THRESHOLD,
        max_compression_artifacts=settings.MAX_COMPRESSION_ARTIFACTS
    )


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
