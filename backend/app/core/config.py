from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API Settings
    PROJECT_NAME: str = "Image Quality Analysis Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str = "imagesvc"
    POSTGRES_PASSWORD: str = "imagesvc"
    POSTGRES_DB: str = "imagesvc"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    @property
    def celery_broker_url(self) -> str:
        return self.CELERY_BROKER_URL or self.REDIS_URL
    
    @property
    def celery_result_backend(self) -> str:
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL
    
    # Storage (Cloudinary/S3)
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    # Storage mode: "local", "cloudinary", or "s3"
    STORAGE_MODE: str = "local"
    UPLOAD_DIR: str = "/tmp/uploads"
    
    # Image validation thresholds
    MAX_FILE_SIZE_MB: int = 10
    MIN_WIDTH: int = 100
    MIN_HEIGHT: int = 100
    MAX_WIDTH: int = 8000
    MAX_HEIGHT: int = 8000
    ALLOWED_FORMATS: list = ["JPEG", "PNG", "WEBP", "GIF"]
    ALLOWED_FORMATS: List = ["JPG", "JPEG", "PNG", "WEBP", "GIF"]

    
    
    # Quality thresholds (placeholder values)
    MIN_QUALITY_SCORE: float = 0.6
    MIN_RESOLUTION_THRESHOLD: int = 500
    MAX_COMPRESSION_ARTIFACTS: float = 0.3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
