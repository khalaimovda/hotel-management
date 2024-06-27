#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start the cronjob in the background
echo "Start fetch data cronjob"
cron &
python manage.py crontab add

# Next commands (Start server)
exec "$@"
