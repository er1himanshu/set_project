from PIL import Image
import io
from typing import Tuple, List, Optional
from app.config import settings


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_image_format(image: Image.Image, filename: str) -> str:
    """Validate image format is allowed"""
    format_lower = image.format.lower() if image.format else ""
    extension = filename.split(".")[-1].lower() if "." in filename else ""
    
    # Check format
    if format_lower not in settings.ALLOWED_IMAGE_FORMATS and extension not in settings.ALLOWED_IMAGE_FORMATS:
        raise ValidationError(
            f"Invalid image format. Allowed formats: {', '.join(settings.ALLOWED_IMAGE_FORMATS)}"
        )
    
    return format_lower or extension


def validate_image_size(image_bytes: bytes) -> None:
    """Validate image file size"""
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_IMAGE_SIZE_MB:
        raise ValidationError(
            f"Image size ({size_mb:.2f} MB) exceeds maximum allowed size ({settings.MAX_IMAGE_SIZE_MB} MB)"
        )


def validate_aspect_ratio(width: int, height: int) -> float:
    """Validate image aspect ratio"""
    aspect_ratio = width / height
    
    if aspect_ratio < settings.MIN_ASPECT_RATIO or aspect_ratio > settings.MAX_ASPECT_RATIO:
        raise ValidationError(
            f"Image aspect ratio ({aspect_ratio:.2f}) is outside allowed range "
            f"({settings.MIN_ASPECT_RATIO} - {settings.MAX_ASPECT_RATIO})"
        )
    
    return aspect_ratio


def validate_resolution(width: int, height: int) -> None:
    """Validate minimum resolution"""
    if width < settings.MIN_RESOLUTION or height < settings.MIN_RESOLUTION:
        raise ValidationError(
            f"Image resolution ({width}x{height}) is below minimum required ({settings.MIN_RESOLUTION}px)"
        )


def validate_image(image_bytes: bytes, filename: str) -> Tuple[Image.Image, dict, List[str]]:
    """
    Complete image validation pipeline
    
    Returns:
        (image, metadata, errors)
    """
    errors = []
    
    try:
        # Validate size
        validate_image_size(image_bytes)
    except ValidationError as e:
        errors.append(str(e))
    
    # Open image
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        errors.append(f"Failed to open image: {str(e)}")
        return None, {}, errors
    
    # Validate format
    try:
        image_format = validate_image_format(image, filename)
    except ValidationError as e:
        errors.append(str(e))
        image_format = "unknown"
    
    # Get dimensions
    width, height = image.size
    
    # Validate aspect ratio
    try:
        aspect_ratio = validate_aspect_ratio(width, height)
    except ValidationError as e:
        errors.append(str(e))
        aspect_ratio = width / height
    
    # Validate resolution
    try:
        validate_resolution(width, height)
    except ValidationError as e:
        errors.append(str(e))
    
    metadata = {
        "format": image_format,
        "width": width,
        "height": height,
        "size_bytes": len(image_bytes),
        "aspect_ratio": aspect_ratio,
    }
    
    return image, metadata, errors
