#!/bin/sh
set -e

export DJANGO_SETTINGS_MODULE=localrestaurantmenus_project.settings.production

# Apply database migrations (a no-op in practice; only for built-in tables)
python manage.py migrate --noinput

# Serve via gunicorn for efficient static + WSGI delivery on Cloud Run.
# WhiteNoise handles static assets (menu images + PDF) inside this same process.
exec gunicorn localrestaurantmenus_project.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --threads 4 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
