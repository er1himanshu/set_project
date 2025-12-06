# System Architecture

## Overview

This document describes the architecture of the Image Quality Analysis and Management System for E-commerce platforms.

## Components

### 1. Backend API (FastAPI)

**Location**: `backend/app/`

**Purpose**: RESTful API for image upload, processing coordination, and result retrieval.

**Key Files**:
- `main.py` - FastAPI application entry point
- `api/routes.py` - API endpoint definitions
- `core/config.py` - Configuration management
- `core/database.py` - Database connection and session management
- `models/image.py` - SQLAlchemy ORM models
- `schemas/image.py` - Pydantic request/response schemas

**API Endpoints**:
- `POST /api/v1/upload/file` - Upload image file
- `POST /api/v1/upload/url` - Upload image from URL
- `GET /api/v1/images` - List all images
- `GET /api/v1/images/{id}` - Get specific image details
- `GET /api/v1/config` - Get configuration thresholds
- `GET /health` - Health check

### 2. Celery Worker

**Location**: `backend/app/worker.py`, `backend/app/tasks/`

**Purpose**: Asynchronous processing of uploaded images.

**Processing Pipeline**:
1. Load image from storage
2. Quality Analysis (placeholder)
3. Compliance Check (placeholder)
4. Compute Embedding (placeholder)
5. Duplicate Detection (placeholder)
6. Update database with results

**Task**: `app.tasks.process_image(image_id: int)`

### 3. Services Layer

**Location**: `backend/app/services/`

**Components**:

#### Validation Service (`validation.py`)
- Format validation
- Size validation (max file size)
- Dimension validation (min/max width/height)
- Aspect ratio checking

#### Quality Analyzer (`quality.py`)
- Quality score computation (placeholder - currently resolution-based)
- Compliance checking (placeholder - basic e-commerce guidelines)
- TODO: Integrate IQA models (BRISQUE, NIQE, deep learning)

#### Similarity Service (`similarity.py`)
- Embedding computation (placeholder - perceptual hash)
- Duplicate detection (placeholder - mock results)
- TODO: Implement FAISS/Annoy for similarity search

#### Storage Service (`storage.py`)
- Local storage implementation
- Cloudinary integration (placeholder)
- S3 integration (placeholder)

### 4. Frontend (React + TypeScript)

**Location**: `frontend/src/`

**Structure**:
```
src/
├── components/          # Reusable UI components
│   ├── UploadForm.tsx   # File/URL upload form
│   ├── ImageTable.tsx   # Results table
│   └── ImageDetailsModal.tsx  # Details modal
├── pages/               # Page components
│   ├── Home.tsx         # Dashboard with upload and results
│   └── Config.tsx       # Configuration display
├── utils/
│   └── api.ts           # API client functions
├── types/
│   └── index.ts         # TypeScript type definitions
├── App.tsx              # Main app with routing
└── main.tsx             # Entry point
```

**Features**:
- Image upload (file or URL)
- Real-time results table (auto-refresh every 5 seconds)
- Detailed results modal
- Configuration display
- Responsive design with Tailwind CSS

### 5. Database (PostgreSQL)

**Schema**: `images` table

**Fields**:
- `id` - Primary key
- `filename` - Image filename
- `original_url` - Source URL (if uploaded from URL)
- `storage_path` - Path to stored image
- `file_size` - File size in bytes
- `width`, `height` - Image dimensions
- `format` - Image format (JPEG, PNG, etc.)
- `status` - Processing status (pending, processing, completed, failed)
- `quality_score` - Quality assessment score (0.0 - 1.0)
- `quality_reasons` - JSON array of quality issues/attributes
- `is_compliant` - Boolean compliance flag
- `compliance_flags` - JSON array of compliance issues
- `is_duplicate` - Boolean duplicate flag
- `duplicate_of_id` - Reference to original image
- `cluster_id` - Similarity cluster identifier
- `embedding_vector` - JSON array (placeholder for actual vector)
- `created_at`, `updated_at`, `processed_at` - Timestamps
- `error_message` - Error details if processing failed

### 6. Message Queue (Redis)

**Purpose**: 
- Celery broker for task distribution
- Result backend for task status/results

## Data Flow

### Upload Flow

```
User -> Frontend -> API -> Database (create record)
                        -> Celery (enqueue task)
                        -> Storage (save file)

Celery Worker -> Load Image -> Process -> Update Database
```

### Processing Flow

```
Celery Task:
1. Fetch image record from database
2. Load image file from storage
3. Run Quality Analysis -> quality_score, quality_reasons
4. Run Compliance Check -> is_compliant, compliance_flags
5. Compute Embedding -> embedding_vector
6. Check Duplicates -> is_duplicate, duplicate_of_id, cluster_id
7. Update database record with results
8. Mark status as 'completed' or 'failed'
```

### Retrieval Flow

```
User -> Frontend -> API -> Database -> Return results
```

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Celery** - Distributed task queue
- **Redis** - Message broker and result backend
- **PostgreSQL** - Relational database
- **Pillow** - Image processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Configuration

Environment variables (`.env`):

### Database
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` - Database credentials
- `POSTGRES_HOST`, `POSTGRES_PORT` - Database connection

### Redis
- `REDIS_HOST`, `REDIS_PORT` - Redis connection

### Storage
- `STORAGE_MODE` - "local", "cloudinary", or "s3"
- `CLOUDINARY_*` - Cloudinary credentials
- `AWS_*` - AWS S3 credentials

### Validation
- `MAX_FILE_SIZE_MB` - Maximum file size
- `MIN_WIDTH`, `MIN_HEIGHT` - Minimum dimensions
- `MAX_WIDTH`, `MAX_HEIGHT` - Maximum dimensions
- `ALLOWED_FORMATS` - List of allowed formats

### Quality Thresholds
- `MIN_QUALITY_SCORE` - Minimum acceptable quality
- `MIN_RESOLUTION_THRESHOLD` - Minimum resolution
- `MAX_COMPRESSION_ARTIFACTS` - Maximum compression artifacts

## Placeholder Components

The following components are implemented with placeholder logic and marked with TODO comments for future implementation:

1. **Quality Analysis** (`services/quality.py`)
   - Currently: Simple resolution-based scoring
   - TODO: Integrate IQA models (BRISQUE, NIQE, CNN-based)

2. **Compliance Checking** (`services/quality.py`)
   - Currently: Basic dimension and aspect ratio checks
   - TODO: Advanced checks (background, watermark, text detection)

3. **Similarity Search** (`services/similarity.py`)
   - Currently: Perceptual hash as fake embedding, mock duplicate detection
   - TODO: Implement deep learning embeddings + FAISS/Annoy index

4. **Cloud Storage** (`services/storage.py`)
   - Currently: Local storage only
   - TODO: Complete Cloudinary and S3 integrations

## Scaling Considerations

### Horizontal Scaling
- API: Multiple FastAPI instances behind load balancer
- Workers: Multiple Celery workers for parallel processing
- Database: PostgreSQL replication for read scaling

### Performance Optimization
- FAISS for efficient similarity search at scale
- Image preprocessing pipeline optimization
- Result caching with Redis
- CDN for image delivery

### Future Enhancements
- Batch processing support
- Image transformation/optimization
- User authentication and authorization
- Rate limiting
- Comprehensive monitoring and logging
- ML model versioning
- A/B testing for quality models

## Security

Current implementation:
- Input validation (file format, size, dimensions)
- CORS configuration for frontend
- Environment variable-based configuration

TODO:
- Authentication and authorization
- API rate limiting
- Input sanitization
- Secure storage configuration
- Audit logging
- Vulnerability scanning

## Testing

Structure for future tests:
```
backend/tests/
├── test_api/
├── test_services/
├── test_models/
└── test_tasks/

frontend/src/__tests__/
├── components/
└── utils/
```

## Monitoring and Logging

Future additions:
- Structured logging with correlation IDs
- Celery task monitoring
- Database query performance monitoring
- API endpoint metrics
- Error tracking (e.g., Sentry)
- APM (Application Performance Monitoring)
