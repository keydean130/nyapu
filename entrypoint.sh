#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python /usr/src/app/nyapu/manage.py flush --no-input
python /usr/src/app/nyapu/manage.py migrate --settings nyapu_pj.settings_dev
python /usr/src/app/nyapu/manage.py loaddata test/test_view
exec "$@"
