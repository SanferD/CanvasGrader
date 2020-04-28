#! /bin/bash

VENV=/opt/python/run/venv/bin/activate
MANAGE=./manage.py
source $VENV
mv server/production_settings.py server/settings.py
$MANAGE makemigrations --noinput
$MANAGE migrate --noinput
$MANAGE collectstatic --noinput

