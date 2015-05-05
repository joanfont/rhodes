#!/bin/bash bash

set -e
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
source /usr/local/bin/virtualenvwrapper.sh
workon rhodes

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

test -d $LOGDIR || mkdir -p $LOGDIR

exec $VIRTUAL_ENV/bin/gunicorn rhodes:app -w $NUM_WORKERS -b 127.0.0.1:8080\
    --user=$USER --group=$GROUP\
    --log-level=info --log-file=$LOGFILE 2>> $LOGERRFILE