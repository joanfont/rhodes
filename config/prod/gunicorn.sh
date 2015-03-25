#!/usr/bin/env bash

set -e
FLASKDIR=/root/rhodes
VIRTUAL_ENV=/root/.virtualenvs/rhodes
USER=root
GROUP=root
LOGFILE=$FLASKDIR/log/gunicorn.log
LOGERRFILE=$FLASKDIR/log/gunicorn_err.log

LOGDIR=$(dirname $LOGFILE)

NUM_WORKERS=3
TIMEOUT=60

cd $FLASKDIR
source $VIRTUAL_ENV/bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

test -d $LOGDIR || mkdir -p $LOGDIR

exec $VIRTUAL_ENV/bin/gunicorn rhodes:app -w $NUM_WORKERS -b 127.0.0.1:8080\
    --user=$USER --group=$GROUP\
    --log-level=info --log-file=$LOGFILE 2>> $LOGERRFILE