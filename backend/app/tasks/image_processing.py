from datetime import datetime
from PIL import Image
from sqlalchemy.orm import Session
from app.worker import celery_app
from app.core.database import SessionLocal
from app.models.image import Image as ImageModel
from app.services.quality import QualityAnalyzer
from app.services.similarity import SimilarityService


@celery_app.task(name="app.tasks.process_image")
def process_image(image_id: int) -> dict:
    """
    Background task to process an uploaded image.
    
    Steps:
    1. Load image from storage
    2. Compute quality analysis (placeholder)
    3. Check compliance (placeholder)
    4. Compute similarity/embedding (placeholder)
    5. Check for duplicates (placeholder)
    6. Update database with results
    """
    db: Session = SessionLocal()
    
    try:
        # Fetch image record
        image_record = db.query(ImageModel).filter(ImageModel.id == image_id).first()
        if not image_record:
            return {"error": f"Image {image_id} not found"}
        
        # Update status to processing
        image_record.status = "processing"
        db.commit()
        
        # Load image file
        if not image_record.storage_path:
            image_record.status = "failed"
            image_record.error_message = "Storage path not found"
            db.commit()
            return {"error": "Storage path not found"}
        
        try:
            img = Image.open(image_record.storage_path)
        except Exception as e:
            image_record.status = "failed"
            image_record.error_message = f"Failed to open image: {str(e)}"
            db.commit()
            return {"error": str(e)}
        
        # 1. Quality Analysis (placeholder)
        quality_score, quality_reasons = QualityAnalyzer.analyze_quality(img)
        image_record.quality_score = quality_score
        image_record.quality_reasons = quality_reasons
        
        # 2. Compliance Check (placeholder)
        is_compliant, compliance_flags = QualityAnalyzer.check_compliance(
            img, 
            {"filename": image_record.filename}
        )
        image_record.is_compliant = is_compliant
        image_record.compliance_flags = compliance_flags
        
        # 3. Compute embedding (placeholder)
        embedding = SimilarityService.compute_embedding(img)
        image_hash = SimilarityService.compute_hash(img)
        image_record.embedding_vector = embedding  # Store as JSON
        
        # 4. Check for duplicates (placeholder)
        is_duplicate, duplicate_of_id, cluster_id = SimilarityService.find_duplicates(
            embedding,
            image_hash
        )
        image_record.is_duplicate = is_duplicate
        image_record.duplicate_of_id = duplicate_of_id
        image_record.cluster_id = cluster_id
        
        # 5. Add to search index (placeholder)
        if not is_duplicate:
            SimilarityService.add_to_index(image_id, embedding)
        
        # Update status to completed
        image_record.status = "completed"
        image_record.processed_at = datetime.utcnow()
        db.commit()
        
        return {
            "image_id": image_id,
            "status": "completed",
            "quality_score": quality_score,
            "is_compliant": is_compliant,
            "is_duplicate": is_duplicate
        }
        
    except Exception as e:
        # Handle any unexpected errors
        if image_record:
            image_record.status = "failed"
            image_record.error_message = str(e)
            db.commit()
        
        return {"error": str(e)}
    
    finally:
        db.close()
