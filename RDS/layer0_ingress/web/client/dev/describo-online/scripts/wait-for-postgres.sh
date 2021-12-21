#!/bin/sh

set -e

if [ "$(which psql)" != 0 ] ; then
    apt-get update && apt-get install -y postgresql-client
fi
cmd="$@"
  
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" postgres -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
  
>&2 echo "Postgres is up - executing command"
exec $cmd
