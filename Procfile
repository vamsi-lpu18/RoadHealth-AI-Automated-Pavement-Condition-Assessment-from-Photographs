web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn roadhealth.wsgi:application --log-file -
worker: celery -A roadhealth worker --loglevel=info
