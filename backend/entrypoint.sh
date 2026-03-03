#!/bin/sh

echo "Waiting for PostgreSQL..."
until python -c "
import sys, os
import psycopg2
try:
    psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'foodgram'),
        user=os.getenv('POSTGRES_USER', 'foodgram'),
        password=os.getenv('POSTGRES_PASSWORD', 'foodgram'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432'),
    ).close()
    sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(1)
" 2>/dev/null; do
    echo "  Database not ready, retrying in 2s..."
    sleep 2
done

echo "Database is ready!"

python manage.py makemigrations users
python manage.py makemigrations recipes
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py load_ingredients

exec gunicorn --bind 0.0.0.0:8000 foodgram.wsgi
