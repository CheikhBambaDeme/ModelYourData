#!/bin/bash
set -e

# ModelYourData - Docker Entrypoint Script

echo "========================================="
echo "   ModelYourData - Starting Container    "
echo "========================================="

# Wait for database to be ready (if using external DB in future)
# sleep 2

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p /app/media/uploads /app/media/results /app/staticfiles /app/db

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "========================================="
echo "   Starting Gunicorn Server              "
echo "   Access at: http://0.0.0.0:80          "
echo "========================================="

# Start Gunicorn
exec gunicorn modelyourdata.wsgi:application \
    --bind 0.0.0.0:80 \
    --workers ${GUNICORN_WORKERS:-2} \
    --threads ${GUNICORN_THREADS:-4} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance
