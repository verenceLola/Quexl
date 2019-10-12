#!/bin/bash -f

# run release commands when releasing the app

python manage.py makemigrations
python manage.py migrate
