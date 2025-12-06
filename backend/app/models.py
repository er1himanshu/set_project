from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class ImageMetadata(Base):
    """Image metadata and processing results"""
    __tablename__ = "image_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_url = Column(Text, nullable=True)
    upload_method = Column(String, nullable=False)  # "file" or "url"
    
    # Storage
    storage_url = Column(Text, nullable=True)
    storage_provider = Column(String, nullable=True)  # "cloudinary", "s3", or "local"
    
    # Image properties
    format = Column(String, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    size_bytes = Column(Integer, nullable=True)
    aspect_ratio = Column(Float, nullable=True)
    
    # Processing status
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    
    # Quality analysis results (placeholder/stub values)
    quality_score = Column(Float, nullable=True)
    quality_reasons = Column(JSON, nullable=True)  # Array of reason strings
    
    # Validation flags
    validation_passed = Column(Boolean, default=True)
    validation_errors = Column(JSON, nullable=True)  # Array of validation error messages
    
    # Compliance flags (stub)
    compliance_passed = Column(Boolean, nullable=True)
    compliance_flags = Column(JSON, nullable=True)  # Array of compliance issue strings
    
    # Duplicate detection (stub)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(Integer, nullable=True)  # Reference to another image_metadata.id
    similarity_score = Column(Float, nullable=True)
    cluster_id = Column(String, nullable=True)  # For grouping similar images
    
    # Embedding/hash for similarity search (placeholder)
    embedding_vector = Column(Text, nullable=True)  # JSON-encoded vector or hash
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "filename": self.filename,
            "original_url": self.original_url,
            "upload_method": self.upload_method,
            "storage_url": self.storage_url,
            "storage_provider": self.storage_provider,
            "format": self.format,
            "width": self.width,
            "height": self.height,
            "size_bytes": self.size_bytes,
            "aspect_ratio": self.aspect_ratio,
            "processing_status": self.processing_status,
            "quality_score": self.quality_score,
            "quality_reasons": self.quality_reasons,
            "validation_passed": self.validation_passed,
            "validation_errors": self.validation_errors,
            "compliance_passed": self.compliance_passed,
            "compliance_flags": self.compliance_flags,
            "is_duplicate": self.is_duplicate,
            "duplicate_of_id": self.duplicate_of_id,
            "similarity_score": self.similarity_score,
            "cluster_id": self.cluster_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }
