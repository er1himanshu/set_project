import os
import shutil
from pathlib import Path
from typing import Optional
from app.core.config import settings


class StorageService:
    """
    Handle image storage (local, Cloudinary, or S3).
    Currently implements local storage with placeholders for cloud services.
    """
    
    @staticmethod
    def save_local(file_path: str, filename: str) -> str:
        """Save file to local storage."""
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        destination = upload_dir / filename
        shutil.copy2(file_path, destination)
        
        return str(destination)
    
    @staticmethod
    def save_to_cloudinary(file_path: str, filename: str) -> Optional[str]:
        """
        Upload to Cloudinary (PLACEHOLDER).
        
        TODO: Implement actual Cloudinary upload.
        """
        if not all([
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET
        ]):
            return None
        
        # Placeholder for Cloudinary upload
        # import cloudinary
        # import cloudinary.uploader
        # 
        # cloudinary.config(
        #     cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        #     api_key=settings.CLOUDINARY_API_KEY,
        #     api_secret=settings.CLOUDINARY_API_SECRET
        # )
        # 
        # result = cloudinary.uploader.upload(file_path, public_id=filename)
        # return result['secure_url']
        
        return f"cloudinary://placeholder/{filename}"
    
    @staticmethod
    def save_to_s3(file_path: str, filename: str) -> Optional[str]:
        """
        Upload to S3 (PLACEHOLDER).
        
        TODO: Implement actual S3 upload using boto3.
        """
        if not all([
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_S3_BUCKET
        ]):
            return None
        
        # Placeholder for S3 upload
        # import boto3
        # 
        # s3_client = boto3.client(
        #     's3',
        #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        #     region_name=settings.AWS_REGION
        # )
        # 
        # s3_client.upload_file(file_path, settings.AWS_S3_BUCKET, filename)
        # return f"s3://{settings.AWS_S3_BUCKET}/{filename}"
        
        return f"s3://placeholder/{filename}"
    
    @classmethod
    def save_image(cls, file_path: str, filename: str) -> str:
        """
        Save image based on configured storage mode.
        Returns storage path/URL.
        """
        if settings.STORAGE_MODE == "cloudinary":
            storage_path = cls.save_to_cloudinary(file_path, filename)
            if storage_path:
                return storage_path
        elif settings.STORAGE_MODE == "s3":
            storage_path = cls.save_to_s3(file_path, filename)
            if storage_path:
                return storage_path
        
        # Fallback to local storage
        return cls.save_local(file_path, filename)
