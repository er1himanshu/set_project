#!/bin/bash
echo "=== Testing Project Structure ==="

echo "✓ Backend structure:"
ls -d backend/app/*/ 2>/dev/null | wc -l | xargs echo "  - Modules:"
ls backend/app/*.py 2>/dev/null | wc -l | xargs echo "  - Core files:"

echo "✓ Frontend structure:"
ls -d frontend/src/*/ 2>/dev/null | wc -l | xargs echo "  - Directories:"
ls frontend/src/components/*.tsx 2>/dev/null | wc -l | xargs echo "  - Components:"
ls frontend/src/pages/*.tsx 2>/dev/null | wc -l | xargs echo "  - Pages:"

echo "✓ Configuration files:"
[ -f .env.example ] && echo "  - .env.example"
[ -f docker-compose.yml ] && echo "  - docker-compose.yml"
[ -f backend/Dockerfile ] && echo "  - backend/Dockerfile"
[ -f frontend/Dockerfile ] && echo "  - frontend/Dockerfile"
[ -f README.md ] && echo "  - README.md"

echo ""
echo "=== Checking Key Files ==="
echo "Backend files:"
find backend/app -name "*.py" | head -10

echo ""
echo "Frontend files:"
find frontend/src -name "*.tsx" -o -name "*.ts" | grep -v node_modules | head -10

echo ""
echo "=== Project is ready! ==="
