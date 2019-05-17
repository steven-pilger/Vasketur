#!/bin/bash
# > /proc/1/fd/1 2>/proc/1/fd/2
# export PATH=/root/.poetry/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# set env variables
set -a > /dev/null
. /.cronenv
set +a > /dev/null

# run querystate management command
cd /code && poetry run python manage.py querystate
