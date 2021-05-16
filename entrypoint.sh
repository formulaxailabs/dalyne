#!/bin/bash

python manage.py wait_for_db
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

if [ "$1" = "celery-worker" ]; then
    echo "starting celery worker"
    celery -A app worker -l info
elif [ "$1" = "celery-beat" ]; then
    echo "starting celery beat"
    celery -A app beat -l info
elif [ "$1" = "gunicorn" ]; then
    echo "starting gunicorn app"
    gunicorn --workers=4 --threads=4 --timeout 600 --bind 0.0.0.0:8000 app.wsgi:application
else
    exec "$@"
fi
