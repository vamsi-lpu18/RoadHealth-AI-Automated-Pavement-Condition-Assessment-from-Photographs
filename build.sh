#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install setuptools first
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media
mkdir -p logs

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
