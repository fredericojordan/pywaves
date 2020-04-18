#!/bin/bash
set -e

if [ "$ENV" = "development" ] ; then
    python docker/web/check_db.py --service-name postgres --ip db --port 5432
    pip install -r requirements/dev.txt

    python src/manage.py migrate
    python src/manage.py collectstatic --noinput
    python src/manage.py runserver 0.0.0.0:8000

else
    python src/manage.py migrate
    python src/manage.py collectstatic --noinput

    echo Starting Gunicorn
    exec gunicorn app.wsgi \
        --bind 0.0.0.0:$PORT \
        --chdir /app/src \
        --workers 3 \
        --log-level=info
fi
