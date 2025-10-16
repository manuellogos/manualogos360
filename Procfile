web: gunicorn manual_cms.wsgi --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput