#!/bin/bash

# Wait for database to be ready
while ! nc -z db 5432; do
    echo "Waiting for database to be ready..."
    sleep 2
done
echo "Database is ready!"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --noinput

# Start the main process
python manage.py runserver 0.0.0.0:8000