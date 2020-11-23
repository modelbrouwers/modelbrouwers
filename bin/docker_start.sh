#!/bin/sh

set -ex

# Wait for the database container
# See: https://docs.docker.com/compose/startup-order/
export PGHOST=${DB_HOST:-db}
export PGPORT=${DB_PORT:-5432}

fixtures_dir=${FIXTURES_DIR:-/app/fixtures}

uwsgi_port=${UWSGI_PORT:-8000}
uwsgi_processes=${UWSGI_PROCESSES:-6}
uwsgi_threads=${UWSGI_THREADS:-5}

until pg_isready; do
  >&2 echo "Waiting for database connection..."
  sleep 1
done

>&2 echo "Database is up."

# Apply database migrations
>&2 echo "Apply database migrations"
python src/manage.py migrate

# Start server
>&2 echo "Starting server"
exec uwsgi \
    --master \
    --http :$uwsgi_port \
    --http-keepalive \
    --module brouwers.wsgi \
    --static-map /static=/app/static \
    --static-map /media=/app/media  \
    --chdir src \
    --enable-threads \
    --threads $uwsgi_threads \
    --post-buffering=8192 \
    --buffer-size=65535 \
    --harakiri 300 \
    --disable-logging \
    --processes $uwsgi_processes \
    --cheaper 2 \
    --cheaper-algo spare \
    --cheaper--initial 4 \
    --cheaper-step 1
