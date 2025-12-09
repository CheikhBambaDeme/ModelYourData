#!/bin/bash
# ModelYourData - Development Run Script
# This script runs Django's development server (for debugging)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   ModelYourData - Development Mode     ${NC}"
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

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Starting Development Server          ${NC}"
echo -e "${GREEN}   Access at: http://127.0.0.1:8000     ${NC}"
echo -e "${GREEN}========================================${NC}"

# Run Django development server
python manage.py runserver
