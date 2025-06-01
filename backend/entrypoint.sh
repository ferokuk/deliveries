#!/bin/sh
set -e

echo "=> Waiting for database…"
sleep 2

echo "=> Applying migrations…"
python3 manage.py migrate --noinput

echo "=> Collecting static files…"
python3 manage.py collectstatic --noinput

echo "=> Creating superuser ‘admin’ (if not exists)…"
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'admin')" \
| python3 manage.py shell

echo "=> Populating database with 1000 entries…"
python3 manage.py populate_db --count=1000

echo "=> Starting server…"
exec python3 manage.py runserver 0.0.0.0:8000
