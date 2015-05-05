from contextlib import contextmanager
import os
from fabric.context_managers import cd, prefix
from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.state import env

from common.environment import Environment

env.hosts = [
    '{user}@{server}'.format(user=Environment.get('SERVER_USER'), server=Environment.get('SERVER_URL'))
]


@contextmanager
def virtualenv():
    with prefix('workon rhodes'):
        yield


@contextmanager
def project_dir(directory=None):
    base_dir = 'echo $PROJECT_DIR'
    if directory:
        base_dir = '{base_dir}/{directory}'.format(base_dir=base_dir, directory=directory
                                                   )
    with cd(run(base_dir)):
        yield


@task
def restart():
    sudo('supervisorctl restart rhodes')
    sudo('service nginx restart')


@task
def pip():
    with virtualenv():
        with project_dir():
            run('pip install -r requirements.txt')


@task
def branch(name):
    switch_branch_command = 'git checkout {branch}'.format(branch=name)
    with virtualenv():
        with project_dir():
            run('git reset --hard')
            run(switch_branch_command)
            run('git pull')


@task
def migrate():
    with virtualenv():
        with cd('application/lib'):
                run('alembic revision --autogenerate')
                run('alembic upgrade head')


@task
def deploy():
    branch('master')
    pip()
    restart()

