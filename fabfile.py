from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.state import env

from config.prod import rhodes as prod_config

import os

env.hosts = ['rhodes.joan-font.com']
env.user = 'root'


@task
def virtualenv():
    run('workon rhodes')


@task
def restart():
    sudo('supervisorctl restart rhodes')
    sudo('service nginx restart')


@task
def branch(name):
    switch_branch_command = 'git checkout {branch}'.format(branch=name)
    with cd(prod_config.PROJECT_DIR):
        run('git reset --hard')
        run(switch_branch_command)
        run('git pull')


@task
def migrate():

    lib_dir = os.path.join(prod_config.PROJECT_DIR, 'application/lib')
    virtualenv()
    with cd(lib_dir):
        run('alembic revision --autogenerate')
        run('alembic upgrade head')


@task
def setup():
    pass


@task
def deploy():
    branch('master')
    restart()

