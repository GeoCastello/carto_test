#!/usr/bin/env bash

if [ "$1" ]; then
    VIRTUALENV_PATH=${1}
    source ${VIRTUALENV_PATH}/bin/activate
fi
FILE_DIR="$(dirname $0)"
cd $FILE_DIR
export DJANGO_READ_DOT_ENV_FILE=True

docker-compose up -d

# Wait 5 secs for the DB to startup, and execute DB scripts
sleep 5

export POSTGRES_MASTER_USER='postgres'
export PGPASSWORD='postgres'

sh create-users.sh
sh create-database.sh
sh grant-permissions.sh
sh add-extensions-to-db.sh

python ../../../manage.py migrate
