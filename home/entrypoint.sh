#!/bin/bash
set -e

echo "🗄️ Migrating..."
python manage.py migrate

echo "📄 Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"