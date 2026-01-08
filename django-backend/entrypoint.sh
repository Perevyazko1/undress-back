#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."

# Ждём доступности базы данных
while ! nc -z pgdb 5432; do
  sleep 1
done

echo "PostgreSQL is up - running migrations and starting server..."

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8003
