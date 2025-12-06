# Image Quality Analysis and Management System for E-commerce

An AI-powered system for analyzing and managing product images for e-commerce platforms. This system provides automated quality assessment, compliance checking, and duplicate detection for images.

## Features

- **Image Upload**: Support for both file upload and URL-based image ingestion
- **Quality Analysis**: Automated quality scoring based on resolution, dimensions, and other factors (placeholder for ML models)
- **Compliance Checking**: Validation against e-commerce guidelines (placeholder for advanced checks)
- **Duplicate Detection**: Similarity-based duplicate identification using embeddings (placeholder for FAISS/Annoy)
- **Real-time Processing**: Asynchronous processing with Celery workers
- **Web Dashboard**: React-based frontend for uploading images and viewing results

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic OpenAPI documentation
- **PostgreSQL**: Relational database for image metadata and results
- **Redis**: Message broker and result backend for Celery
- **Celery**: Distributed task queue for asynchronous processing
- **SQLAlchemy**: ORM for database operations
- **Pillow**: Image processing library

### Frontend
- **React**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client

### Infrastructure
- **Docker Compose**: Container orchestration for local development

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│   Frontend  │────▶│   FastAPI    │────▶│  Celery   │
│  (React)    │◀────│   Backend    │     │  Worker   │
└─────────────┘     └──────────────┘     └───────────┘
                           │                    │
                           ▼                    ▼
                    ┌──────────────┐     ┌───────────┐
                    │  PostgreSQL  │     │   Redis   │
                    └──────────────┘     └───────────┘
```

## Setup and Installation

### Prerequisites
- Docker and Docker Compose (recommended)
- OR Python 3.11+, Node.js 18+, PostgreSQL, and Redis (for local development)

### Quick Start with Docker Compose

1. **Clone the repository**
   ```bash
   git clone https://github.com/er1himanshu/set_project.git
   cd set_project
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work for Docker Compose)
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - Backend API (http://localhost:8000)
   - Celery Worker
   - PostgreSQL Database
   - Redis
   - Frontend (http://localhost:5173)

4. **Access the application**
   - Frontend UI: http://localhost:5173
   - API Documentation: http://localhost:8000/docs
   - API Health Check: http://localhost:8000/health

### Local Development (Without Docker)

#### Backend Setup

1. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   # Update .env with local settings:
   POSTGRES_HOST=localhost
   REDIS_HOST=localhost
   ```

3. **Start PostgreSQL and Redis**
   ```bash
   # Using Docker for just the databases:
   docker run -d -p 5432:5432 -e POSTGRES_DB=imagesvc -e POSTGRES_USER=imagesvc -e POSTGRES_PASSWORD=imagesvc postgres:15
   docker run -d -p 6379:6379 redis:7
   ```

4. **Start the API server**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

5. **Start the Celery worker** (in another terminal)
   ```bash
   cd backend
   celery -A app.worker.celery_app worker --loglevel=info
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API URL**
   ```bash
   # Create .env in frontend directory
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

3. **Start the dev server**
   ```bash
   npm run dev
   ```

## Usage

### Uploading Images

#### Via Web UI
1. Navigate to http://localhost:5173
2. Use the upload form to either:
   - Upload a file from your computer
   - Provide a URL to an image
3. View the image in the results table
4. Click "Details" to see full analysis results

#### Via API

**Upload a file:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload/file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

**Upload from URL:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/image.jpg"}'
```

### Viewing Results

**List all images:**
```bash
curl "http://localhost:8000/api/v1/images"
```

**Get specific image details:**
```bash
curl "http://localhost:8000/api/v1/images/1"
```

**Get configuration:**
```bash
curl "http://localhost:8000/api/v1/config"
```

### Demo Script

Here's a complete workflow example:

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. Upload a test image
curl -X POST "http://localhost:8000/api/v1/upload/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://picsum.photos/1200/1200"}'

# 3. Wait a few seconds for processing

# 4. List all images
curl http://localhost:8000/api/v1/images

# 5. Get specific image details (replace 1 with actual ID)
curl http://localhost:8000/api/v1/images/1

# 6. View configuration
curl http://localhost:8000/api/v1/config
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Project Structure

```
set_project/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Core configuration
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── tasks/         # Celery tasks
│   │   ├── main.py        # FastAPI application
│   │   └── worker.py      # Celery configuration
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── types/         # TypeScript types
│   │   ├── utils/         # Utility functions
│   │   ├── App.tsx        # Main app component
│   │   └── main.tsx       # Entry point
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## Configuration

Key environment variables (see `.env.example` for full list):

- `POSTGRES_*`: Database connection settings
- `REDIS_*`: Redis connection settings
- `STORAGE_MODE`: Storage backend (`local`, `cloudinary`, or `s3`)
- `MAX_FILE_SIZE_MB`: Maximum allowed file size
- `MIN_QUALITY_SCORE`: Minimum acceptable quality score
- `VITE_API_URL`: Frontend API endpoint

## Roadmap

### Current Status (v1.0 - Placeholder Implementation)
- ✅ Basic API structure with FastAPI
- ✅ File and URL upload endpoints
- ✅ Basic validation (format, size, dimensions)
- ✅ PostgreSQL database for metadata
- ✅ Celery worker for async processing
- ✅ Placeholder quality analysis
- ✅ Placeholder compliance checking
- ✅ Placeholder duplicate detection
- ✅ React frontend with Tailwind CSS
- ✅ Docker Compose setup

### Future Enhancements
- 🔄 Integrate actual IQA models (BRISQUE, NIQE, or deep learning)
- 🔄 Implement real duplicate detection with FAISS/Annoy
- 🔄 Add advanced compliance rules (background detection, watermark detection)
- 🔄 Implement batch processing
- 🔄 Add image optimization/transformation
- 🔄 Implement user authentication
- 🔄 Add analytics dashboard
- 🔄 Cloud storage integration (Cloudinary/S3)
- 🔄 Add comprehensive test coverage
- 🔄 Performance monitoring and logging

## Troubleshooting

### Port already in use
If ports 8000, 5173, 5432, or 6379 are already in use, either stop the conflicting services or modify the port mappings in `docker-compose.yml`.

### Database connection errors
Ensure PostgreSQL is running and the credentials in `.env` match your database configuration.

### Worker not processing jobs
Check that:
1. Redis is running
2. The Celery worker is started
3. Environment variables are correctly set

### Frontend can't connect to API
Verify that:
1. Backend is running on port 8000
2. `VITE_API_URL` in frontend `.env` points to the correct backend URL
3. CORS is configured correctly (already handled in development)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.
