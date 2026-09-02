#!/usr/bin/env bash
set -e

echo "========================================"
echo "Installing Python dependencies"
echo "========================================"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "========================================"
echo "Collecting static files"
echo "========================================"

python manage.py collectstatic --noinput

echo "========================================"
echo "Running database migrations"
echo "========================================"

python manage.py migrate

echo "========================================"
echo "BUILD COMPLETE"
echo "========================================"