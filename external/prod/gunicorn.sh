#!/usr/bin/env bash

set -e
FLASKDIR=/home/ubuntu/rhodes
VIRTUAL_ENV=/home/ubuntu/.virtualenvs/rhodes
USER=ubuntu
GROUP=ubuntu
LOGFILE=$FLASKDIR/log/gunicorn.log
LOGERRFILE=$FLASKDIR/log/gunicorn_err.log

LOGDIR=$(dirname $LOGFILE)

NUM_WORKERS=2

cd $FLASKDIR
source $VIRTUAL_ENV/bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

test -d $LOGDIR || mkdir -p $LOGDIR

exec $VIRTUAL_ENV/bin/gunicorn rhodes:app -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --log-level=warning \
  --log-file=$LOGFILE -b 127.0.0.1:8080 2>> $LOGERRFILE