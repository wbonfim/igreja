#!/bin/sh

set -e

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done
echo "PostgreSQL started"

echo "Waiting for redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 1
done
echo "Redis started"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating initial data..."
python manage.py criar_usuario_padrao
python manage.py criar_templates_padrao
python manage.py criar_igreja_padrao

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class gthread \
    --threads 4 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --reload
