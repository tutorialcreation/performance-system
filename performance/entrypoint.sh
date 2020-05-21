#!/bin/bash
#python manage.py test
#python manage.py makemigrations
# source /root/.local/share/virtualenvs/performance_system-*/bin/activate
pipenv shell
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
exec "$@"


