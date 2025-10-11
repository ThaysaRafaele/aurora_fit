#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install poetry
poetry config virtualenvs.create false
poetry install --no-dev
python manage.py collectstatic --no-input
python manage.py migrate
