#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh
workon rhodes

FLASKDIR=$PROJECT_DIR
VIRTUAL_ENV=$VENV_DIR
USER=root
GROUP=root
LOGFILE=$FLASKDIR/log/gunicorn.log
LOGERRFILE=$FLASKDIR/log/gunicorn_err.log

LOGDIR=$(dirname $LOGFILE)

NUM_WORKERS=3
TIMEOUT=60

cd $FLASKDIR
export PYTHONPATH=$FLASKDIR:$PYTHONPATH

test -d $LOGDIR || mkdir -p $LOGDIR

exec gunicorn rhodes:app -w $NUM_WORKERS -b 127.0.0.1:8080\
    --user=$USER --group=$GROUP\
    --log-level=info --log-file=$LOGFILE 2>> $LOGERRFILE