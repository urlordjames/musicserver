#!/bin/sh

python manage.py makemigrations
python manage.py migrate
gunicorn -b 0.0.0.0:8000 musicserver.wsgi