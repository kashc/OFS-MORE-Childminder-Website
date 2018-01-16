#!/bin/bash

# Create database migration files
echo "Create database migration files"
python manage.py makemigrations
python manage.py makemigrations application

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
python manage.py migrate application

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000