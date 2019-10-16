#!/bin/bash

# Create super user?

echo "Creating model migrations"
python3 manage.py makemigrations --settings=autoscheduler.settings.docker scraper

echo "Migrating models"
python3 manage.py migrate --settings=autoscheduler.settings.docker
python3 manage.py migrate --settings=autoscheduler.settings.docker scraper

echo "Starting tests"
# python3 manage.py runserver --settings=autoscheduler.settings.docker 0.0.0.0:8000
python3 manage.py test --settings=autoscheduler.settings.docker