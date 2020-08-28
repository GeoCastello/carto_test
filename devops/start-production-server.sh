#!/bin/sh

set -o errexit

/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:5000 --workers=9 --timeout=45 --chdir=/app --log-file=-
