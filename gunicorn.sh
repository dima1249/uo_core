#!/bin/bash

NAME="uo back"                               # Name of the application (*)
DJANGODIR=/var/www/uo_core                 # Django project directory (*)
SOCKFILE=/var/www/uo_core/run/gunicorn.sock # we will communicate using this unix socket (*)
USER=nginx                               # the user to run as (*)
GROUP=webdata                            # the group to run as (*)
NUM_WORKERS=1                            # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=uo_core.settings      # which settings file should Django use (*)
DJANGO_WSGI_MODULE=uo_core.wsgi              # WSGI module name (*)

echo "Starting $NAME as $(whoami)"

# Activate the virtual environment
cd $DJANGODIR
source /var/www/uo_core/env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --bind=unix:$SOCKFILE \
  --workers=$NUM_WORKERS
