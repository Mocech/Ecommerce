#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Adjust path to manage.py if it is in a subfolder
python Grocery/vages/manage.py collectstatic --no-input
python Grocery/vages/manage.py migrate

if [[ $CREATE_SUPERUSER ]]; then
  python Grocery/vages/manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi
