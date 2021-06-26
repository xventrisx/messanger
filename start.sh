#!/bin/bash
set -e

# Load base data
python manage.py migrate --noinput

if [[ $DJANGO_DEBUG -eq 0 ]]; then
  # production mode
  python manage.py collectstatic --noinput
  gunicorn -w 4 --env DJANGO_SETTINGS_MODULE=_project_.settings _project_.wsgi -b 0.0.0.0:8000
else
  # development mode
  python manage.py runserver 0.0.0.0:8000
fi