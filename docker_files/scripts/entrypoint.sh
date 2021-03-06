#!/bin/sh

set -e

python wait.py
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-threads --module core.wsgi
