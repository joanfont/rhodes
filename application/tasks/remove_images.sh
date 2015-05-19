#!/bin/bash
export WORKON_HOME=~/.virtualenvs/
source /usr/local/bin/virtualenvwrapper.sh
workon rhodes

python $PROJECT_DIR/rhodes.py remove_images