#!/bin/sh
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

cp -r collected_static/. /backend_static/static/

DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_EMAIL="admin@admin.ru" \
python manage.py createsuperuser --noinput

gunicorn --reload -b 0.0.0.0:8000 alpha_project.wsgi