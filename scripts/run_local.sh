#!/usr/bin/env bash

# Script to run the Django server in a development environment

python3 manage.py migrate
python3 quick_test_seeding.py
python3 manage.py runserver 0.0.0.0:8001