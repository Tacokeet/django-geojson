#!/bin/bash

while ! nc -z db 5432; do
    echo "Waiting for database to be ready..."
    sleep 2
done

# Start the main process
python manage.py test