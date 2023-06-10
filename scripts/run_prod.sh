#!/usr/bin/env bash

# Script to run the Django server in a production environment

python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear
python3 quick_test_seeding.py
gunicorn --bind :8002 --workers 3 bookstoreapi.wsgi:application
