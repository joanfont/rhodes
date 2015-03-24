#!/usr/bin/env bash

set -e
FLASKDIR=/Users/joanfont/Developer/Python/rhodes
VIRTUAL_ENV=/Users/joanfont/.virtualenvs/rhodes
USER=joanfont
GROUP=staff
LOGFILE=$FLASKDIR/log/gunicorn.log
LOGERRFILE=$FLASKDIR/log/gunicorn_err.log

LOGDIR=$(dirname $LOGFILE)

NUM_WORKERS=2
TIMEOUT=60

cd $FLASKDIR
source $VIRTUAL_ENV/bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

test -d $LOGDIR || mkdir -p $LOGDIR

exec $VIRTUAL_ENV/bin/gunicorn rhodes:app -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --timeout $TIMEOUT --log-level=warning \
  --log-file=$LOGFILE -b 127.0.0.1:8080 2>> $LOGERRFILE