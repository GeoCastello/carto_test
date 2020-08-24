#!/usr/bin/env bash

set -e

psql -v ON_ERROR_STOP=1 --host localhost --username $POSTGRES_MASTER_USER -f create_users.sql