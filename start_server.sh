#!/bin/bash

# Activate your virtual environment
source .venv/bin/activate

# Start the Django server
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.local
