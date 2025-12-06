from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Image Quality Analysis System"
    DEBUG: bool = True
    
    # Database
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "imagesvc"
    POSTGRES_USER: str = "imagesvc"
    POSTGRES_PASSWORD: str = "imagesvc"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"
    
    # Cloud Storage (Cloudinary)
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    
    # Cloud Storage (S3)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    # Image Validation
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_IMAGE_FORMATS: list = ["jpg", "jpeg", "png", "webp"]
    MIN_ASPECT_RATIO: float = 0.5
    MAX_ASPECT_RATIO: float = 2.0
    MIN_RESOLUTION: int = 300
    
    # Quality Thresholds
    MIN_QUALITY_SCORE: float = 0.6
    MIN_SHARPNESS_SCORE: float = 0.5
    MIN_BRIGHTNESS_SCORE: float = 0.4
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
