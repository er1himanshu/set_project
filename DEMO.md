# Demo Guide

This guide walks you through using the Image Quality Analysis System.

## Starting the Application

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Terminal 1 - Database & Redis:**
```bash
docker run -d -p 5432:5432 -e POSTGRES_DB=imagesvc -e POSTGRES_USER=imagesvc -e POSTGRES_PASSWORD=imagesvc postgres:15
docker run -d -p 6379:6379 redis:7
```

**Terminal 2 - Backend API:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 - Celery Worker:**
```bash
cd backend
celery -A app.worker.celery_app worker --loglevel=info
```

**Terminal 4 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Using the Web Interface

### 1. Dashboard (Home Page)

Navigate to http://localhost:5173

**Features:**
- Upload form (left panel)
- Quick stats (right panel)
- Results table (bottom)

**Upload Options:**
- **File Upload**: Click "Upload File" tab, select an image from your computer
- **URL Upload**: Click "From URL" tab, paste an image URL

### 2. Upload an Image

**Example File Upload:**
1. Click "Upload File" tab
2. Click the file input and select an image (JPEG, PNG, WEBP, or GIF)
3. Click "Upload" button
4. You'll see a success message with the image ID
5. The image appears in the table below with status "pending" or "processing"

**Example URL Upload:**
1. Click "From URL" tab
2. Enter an image URL, e.g.: `https://picsum.photos/1200/1200`
3. Click "Upload" button
4. The image is downloaded, validated, and queued for processing

### 3. View Results

The results table shows:
- **ID**: Unique image identifier
- **Filename**: Original or generated filename
- **Dimensions**: Width × Height in pixels
- **Status**: pending → processing → completed (or failed)
- **Quality Score**: 0.00 to 1.00 (computed by placeholder algorithm)
- **Compliant**: ✓ Yes or ✗ No (based on e-commerce guidelines)
- **Duplicate**: ⚠ Yes or No (placeholder detection)
- **Actions**: "Details" button

**Status Colors:**
- 🟢 Green: Completed
- 🟡 Yellow: Processing/Pending
- 🔴 Red: Failed
- ⚪ Gray: Pending

### 4. View Image Details

Click the "Details" button for any image to see:

**Basic Information:**
- ID, Status, Filename
- Original URL (if uploaded from URL)
- Format, File Size
- Dimensions
- Upload timestamp

**Quality Analysis:**
- Quality Score (with color coding)
- Reasons for the score (e.g., "High resolution", "Good resolution", "Low resolution")

**Compliance Check:**
- Is Compliant: Yes/No
- Flags (e.g., "Below recommended e-commerce size", "Non-square aspect ratio")

**Duplicate Detection:**
- Is Duplicate: Yes/No
- Duplicate Of ID (if duplicate)
- Cluster ID (similarity grouping)

**Error Information:**
- Error message (if processing failed)

### 5. Configuration Page

Navigate to "Configuration" in the top menu

**Displays:**

**Image Validation:**
- Max File Size: 10 MB
- Min Dimensions: 100 × 100
- Max Dimensions: 8000 × 8000
- Allowed Formats: JPEG, PNG, WEBP, GIF

**Quality Analysis Thresholds:**
- Min Quality Score: 0.6
- Min Resolution: 500px
- Max Compression Artifacts: 0.3

## API Examples

### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy"}
```

### Upload from URL
```bash
curl -X POST "http://localhost:8000/api/v1/upload/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://picsum.photos/1200/1200"}'

# Response:
# {
#   "id": 1,
#   "filename": "abc123.jpg",
#   "status": "pending",
#   "message": "Image uploaded successfully and queued for processing"
# }
```

### Upload File
```bash
curl -X POST "http://localhost:8000/api/v1/upload/file" \
  -F "file=@/path/to/image.jpg"

# Response: Same as URL upload
```

### List All Images
```bash
curl http://localhost:8000/api/v1/images

# Response: Array of image objects
```

### Get Specific Image
```bash
curl http://localhost:8000/api/v1/images/1

# Response:
# {
#   "id": 1,
#   "filename": "abc123.jpg",
#   "status": "completed",
#   "quality_score": 0.75,
#   "quality_reasons": ["Good resolution"],
#   "is_compliant": false,
#   "compliance_flags": ["Below recommended e-commerce size (800x800)"],
#   "is_duplicate": false,
#   ...
# }
```

### Get Configuration
```bash
curl http://localhost:8000/api/v1/config

# Response: Configuration object with all thresholds
```

### Interactive API Documentation
Visit http://localhost:8000/docs for Swagger UI with:
- Complete API reference
- Try-it-out functionality
- Request/response schemas
- Authentication (when added)

## Example Workflow

### Complete Test Scenario

```bash
# 1. Check system health
curl http://localhost:8000/health

# 2. Upload a high-quality image
curl -X POST "http://localhost:8000/api/v1/upload/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://picsum.photos/1200/1200"}'
# Save the returned ID (e.g., 1)

# 3. Wait 2-3 seconds for processing

# 4. Check the image details
curl http://localhost:8000/api/v1/images/1

# 5. Upload a low-quality image
curl -X POST "http://localhost:8000/api/v1/upload/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://picsum.photos/400/400"}'

# 6. List all images
curl http://localhost:8000/api/v1/images

# 7. Check configuration
curl http://localhost:8000/api/v1/config
```

## Expected Results

### High Quality Image (1200×1200)
- **Quality Score**: ~0.75-0.90
- **Quality Reasons**: "High resolution", "Good resolution"
- **Compliant**: Yes (if square and large enough)
- **Status**: Completed

### Low Quality Image (400×400)
- **Quality Score**: ~0.4-0.6
- **Quality Reasons**: "Low resolution", "Small dimensions"
- **Compliant**: No
- **Compliance Flags**: "Below recommended e-commerce size (800x800)"
- **Status**: Completed

### Invalid Image
- **Status**: Failed
- **Error Message**: Validation error details

## Troubleshooting

### Image stays in "pending" status
- Check that Celery worker is running
- Check worker logs for errors
- Verify Redis connection

### Upload fails
- Check image format (must be JPEG, PNG, WEBP, or GIF)
- Check file size (max 10 MB)
- Check dimensions (min 100×100, max 8000×8000)
- For URL uploads, ensure URL is accessible

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify VITE_API_URL in frontend .env

## Next Steps

This is a scaffold implementation with placeholder logic for:
- Quality analysis (currently resolution-based)
- Compliance checking (basic e-commerce rules)
- Duplicate detection (mock implementation)

To make it production-ready:
1. Integrate actual IQA models (BRISQUE, NIQE, or CNN-based)
2. Implement real duplicate detection with FAISS
3. Add advanced compliance checks (background, watermark detection)
4. Set up cloud storage (Cloudinary or S3)
5. Add authentication and authorization
6. Implement batch processing
7. Add comprehensive testing
8. Set up monitoring and logging
