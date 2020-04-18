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

    # Prepare log files and start outputting logs to stdout
    mkdir -p /srv/logs/
    touch /srv/logs/gunicorn.log
    touch /srv/logs/access.log
    tail -n 0 -f /srv/logs/*.log &

    echo Starting Gunicorn
    exec gunicorn app.wsgi \
        --bind 0.0.0.0:8000 \
        --chdir /usr/src/app/src \
        --workers 3 \
        --log-level=info \
        --log-file=/srv/logs/gunicorn.log \
        --access-logfile=/srv/logs/access.log
fi
