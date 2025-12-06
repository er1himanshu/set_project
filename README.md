# AI-Powered Image Quality Analysis and Management System

A modern end-to-end solution for image quality analysis, compliance checking, and duplicate detection for e-commerce platforms.

![System Status](https://github.com/user-attachments/assets/99c2a952-5a4c-4b9c-8d2f-6aea64095db3)

## Features

- **Image Upload**: Support for both file upload and URL-based image ingestion
- **Quality Analysis**: AI-powered image quality assessment with detailed scoring
- **Compliance Checking**: Automated compliance validation against e-commerce guidelines
- **Duplicate Detection**: Similarity-based duplicate image detection and clustering
- **Real-time Processing**: Asynchronous job processing with Celery and Redis
- **Modern UI**: React + Vite + Tailwind CSS frontend with real-time updates
- **REST API**: FastAPI-based backend with OpenAPI documentation

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **PostgreSQL**: Database for storing image metadata and processing results
- **Celery**: Distributed task queue for asynchronous processing
- **Redis**: Message broker and result backend for Celery
- **SQLAlchemy**: ORM for database operations
- **Pillow**: Image processing library

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client

### DevOps
- **Docker & Docker Compose**: Containerization and orchestration
- **Uvicorn**: ASGI server for FastAPI

## Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB of available RAM

### Setup and Run

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd set_project
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

## Local Development Setup (Without Docker)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your local configuration
   ```

5. **Start PostgreSQL and Redis** (if not using Docker)
   ```bash
   # Using Docker for just databases:
   docker run -d -p 5432:5432 -e POSTGRES_DB=imagesvc -e POSTGRES_USER=imagesvc -e POSTGRES_PASSWORD=imagesvc postgres:15
   docker run -d -p 6379:6379 redis:7
   ```

6. **Run the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Start the Celery worker** (in a separate terminal)
   ```bash
   cd backend
   source venv/bin/activate
   celery -A app.worker.celery_app worker --loglevel=info
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:5173

## API Endpoints

### Upload Endpoints

#### Upload Image File
```bash
POST /api/images/upload/file
Content-Type: multipart/form-data

# Example with curl:
curl -X POST "http://localhost:8000/api/images/upload/file" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

#### Upload Image from URL
```bash
POST /api/images/upload/url
Content-Type: application/json

# Example:
curl -X POST "http://localhost:8000/api/images/upload/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/image.jpg"}'
```

### Query Endpoints

#### List All Images
```bash
GET /api/images?skip=0&limit=100
```

#### Get Image Details
```bash
GET /api/images/{image_id}
```

#### Get Processing Result
```bash
GET /api/images/{image_id}/result
```

#### Get Configuration
```bash
GET /api/config
```

#### Delete Image
```bash
DELETE /api/images/{image_id}
```

## Demo Script

### Testing the Upload Endpoint

1. **Upload a test image via file**
   ```bash
   # Create a test image (if you don't have one)
   curl -o test_image.jpg "https://picsum.photos/1200/800"
   
   # Upload it
   curl -X POST "http://localhost:8000/api/images/upload/file" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg"
   ```

2. **Upload an image via URL**
   ```bash
   curl -X POST "http://localhost:8000/api/images/upload/url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://picsum.photos/1024/768"}'
   ```

3. **Check processing status**
   ```bash
   # List all images
   curl "http://localhost:8000/api/images"
   
   # Get specific image details (replace {id} with actual ID)
   curl "http://localhost:8000/api/images/1"
   
   # Get processing result
   curl "http://localhost:8000/api/images/1/result"
   ```

4. **View configuration**
   ```bash
   curl "http://localhost:8000/api/config"
   ```

### Testing the UI

1. **Open the frontend** at http://localhost:5173

2. **Upload an image**
   - Click "Upload File" or "Upload from URL"
   - Select a file or enter a URL
   - Click "Upload Image"

3. **View results**
   - The image will appear in the table with status "pending"
   - After ~2-3 seconds, status will change to "completed"
   - Click "View Details" to see full analysis results

4. **Check configuration**
   - Click "Configuration" in the navigation
   - View current validation rules and quality thresholds

## Architecture

### System Components

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  PostgreSQL │
│ React+Vite  │     │   FastAPI   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Redis    │
                    │   Broker    │
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Celery    │
                    │   Worker    │
                    └─────────────┘
```

### Processing Flow

1. **Upload**: User uploads image via frontend or API
2. **Validation**: Backend validates format, size, aspect ratio, resolution
3. **Storage**: Metadata saved to PostgreSQL
4. **Queue**: Processing job queued to Celery via Redis
5. **Processing**: Worker performs quality analysis, compliance check, duplicate detection
6. **Results**: Results written back to PostgreSQL
7. **Display**: Frontend polls for updates and displays results

## Stub Implementations & TODOs

The current implementation includes placeholder/stub functions for ML-based features:

### Quality Analysis (`app/processing.py`)
- **Current**: Random score generation with placeholder reasons
- **TODO**: Integrate actual IQA model (BRISQUE, NIQE, or deep learning model)

### Compliance Checking (`app/processing.py`)
- **Current**: Basic rule checks with random flags
- **TODO**: Implement:
  - Brand guideline validation
  - Inappropriate content detection
  - Copyright/watermark detection
  - Text overlay rule enforcement

### Duplicate Detection (`app/processing.py`)
- **Current**: Random duplicate detection with fake embeddings
- **TODO**: Integrate:
  - Pre-trained CNN for feature extraction (ResNet, EfficientNet)
  - FAISS or Annoy index for efficient similarity search
  - Proper cosine similarity or L2 distance computation

### Cloud Storage
- **Current**: Placeholder for Cloudinary and S3
- **TODO**: Implement actual upload to cloud storage with signed URLs

## Environment Variables

See `.env.example` for all available configuration options:

- **Database**: PostgreSQL connection settings
- **Redis**: Redis connection for Celery
- **Storage**: Cloudinary and S3 credentials (optional)
- **Validation**: Image validation rules
- **Thresholds**: Quality score thresholds

## Troubleshooting

### Port Already in Use
If you see "port already in use" errors:
```bash
# Kill processes on specific ports
# On Linux/Mac:
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend
lsof -ti:5432 | xargs kill -9  # PostgreSQL
lsof -ti:6379 | xargs kill -9  # Redis
```

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Recreate database
docker-compose down -v
docker-compose up -d db
```

### Worker Not Processing Jobs
```bash
# Check worker logs
docker-compose logs worker

# Restart worker
docker-compose restart worker
```

### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
