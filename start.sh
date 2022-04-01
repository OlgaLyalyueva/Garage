#!/bin/sh

sleep 10
python manage.py makemigrations --noinput --settings=Garage.settings_${ENV:=staging}
python manage.py migrate --noinput --settings=Garage.settings_${ENV:=staging}
python manage.py collectstatic --noinput --settings=Garage.settings_${ENV:=staging}
python manage.py runserver --settings=Garage.settings_${ENV:=staging} 0.0.0.0:8000