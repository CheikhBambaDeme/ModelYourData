#!/bin/bash
# ModelYourData - Run Script
# This script sets up and runs the Django application with Gunicorn

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   ModelYourData - Starting Server      ${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p media/uploads media/results staticfiles

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Starting Gunicorn Server             ${NC}"
echo -e "${GREEN}   Access at: http://127.0.0.1:8000     ${NC}"
echo -e "${GREEN}========================================${NC}"

# Run with Gunicorn
gunicorn modelyourdata.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance
