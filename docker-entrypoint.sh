#!/bin/sh

echo "Installing missing dependencies"
pip install -Ur requirements.txt

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Generate translations
echo "Create translations"
django-admin compilemessages

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
