#!/bin/sh
set -e

echo "=> Waiting for database…"
# если нужно — можно подключить wait-for-it.sh или просто sleep
sleep 2

echo "=> Applying migrations…"
python3 manage.py migrate --noinput

echo "=> Starting server…"
exec python3 manage.py runserver 0.0.0.0:8000
