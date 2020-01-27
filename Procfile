release: django-admin compilemessages && python manage.py migrate
web: gunicorn seawatch_planner.wsgi --log-file -