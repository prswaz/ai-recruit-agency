#!/bin/bash

# Wait for database if needed (optional but recommended for production)
# echo "Waiting for SQL Server..."
# while ! nc -z $DB_HOST $DB_PORT; do
#   sleep 0.1
# done
# echo "SQL Server started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn ai_recruiter_django.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
