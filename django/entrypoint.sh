#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

pipenv run python /usr/src/nyapu/manage.py flush --no-input
pipenv run python /usr/src/nyapu/manage.py migrate --settings nyapu_pj.settings_dev
pipenv run python /usr/src/nyapu/manage.py loaddata test/test_data

exec "$@"
