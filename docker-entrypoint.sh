#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate

exec gunicorn --bind 0.0.0.0:8000 interview_scheduler.wsgi:application
