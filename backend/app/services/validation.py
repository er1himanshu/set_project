from PIL import Image
from typing import Tuple, Optional
from app.core.config import settings


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ImageValidator:
    """Validates images based on configured thresholds."""
    
    @staticmethod
    def validate_format(image: Image.Image) -> None:
        """Validate image format."""
        if image.format not in settings.ALLOWED_FORMATS:
            raise ValidationError(
                f"Invalid format {image.format}. Allowed: {', '.join(settings.ALLOWED_FORMATS)}"
            )
    
    @staticmethod
    def validate_size(file_size: int) -> None:
        """Validate file size."""
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise ValidationError(
                f"File size {file_size} bytes exceeds maximum {max_bytes} bytes"
            )
    
    @staticmethod
    def validate_dimensions(width: int, height: int) -> None:
        """Validate image dimensions."""
        if width < settings.MIN_WIDTH or height < settings.MIN_HEIGHT:
            raise ValidationError(
                f"Image dimensions {width}x{height} below minimum "
                f"{settings.MIN_WIDTH}x{settings.MIN_HEIGHT}"
            )
        
        if width > settings.MAX_WIDTH or height > settings.MAX_HEIGHT:
            raise ValidationError(
                f"Image dimensions {width}x{height} exceed maximum "
                f"{settings.MAX_WIDTH}x{settings.MAX_HEIGHT}"
            )
    
    @staticmethod
    def validate_aspect_ratio(width: int, height: int) -> Tuple[bool, Optional[str]]:
        """
        Validate aspect ratio (placeholder - returns warning only).
        Returns: (is_valid, warning_message)
        """
        aspect_ratio = width / height
        # Placeholder: warn about extreme aspect ratios
        if aspect_ratio < 0.2 or aspect_ratio > 5.0:
            return True, f"Unusual aspect ratio: {aspect_ratio:.2f}"
        return True, None
    
    @classmethod
    def validate_image(cls, image: Image.Image, file_size: int) -> Tuple[bool, list]:
        """
        Validate image against all rules.
        Returns: (is_valid, warnings_list)
        """
        warnings = []
        
        try:
            cls.validate_format(image)
            cls.validate_size(file_size)
            cls.validate_dimensions(image.width, image.height)
            
            # Check aspect ratio (non-blocking)
            _, aspect_warning = cls.validate_aspect_ratio(image.width, image.height)
            if aspect_warning:
                warnings.append(aspect_warning)
            
            return True, warnings
            
        except ValidationError as e:
            raise e
