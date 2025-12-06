from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Image(Base):
    """Image metadata and analysis results."""
    
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_url = Column(String, nullable=True)
    storage_path = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)  # bytes
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    format = Column(String, nullable=True)
    
    # Processing status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    
    # Quality analysis results (placeholder)
    quality_score = Column(Float, nullable=True)
    quality_reasons = Column(JSON, nullable=True)  # Array of reason strings
    
    # Compliance flags (placeholder)
    is_compliant = Column(Boolean, default=None, nullable=True)
    compliance_flags = Column(JSON, nullable=True)  # Array of flag strings
    
    # Duplicate detection (placeholder)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(Integer, nullable=True)
    cluster_id = Column(String, nullable=True)
    embedding_vector = Column(JSON, nullable=True)  # Placeholder for actual vector
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Error tracking
    error_message = Column(String, nullable=True)
