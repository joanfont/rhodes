import os
from contextlib import contextmanager

from fabric.context_managers import cd, prefix
from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.state import env

from common.environment import Environment


from dotenv import load_dotenv
load_dotenv('.env')


env.hosts = [
    '{user}@{server}'.format(user=Environment.get('SERVER_USER'), server=Environment.get('SERVER_URL'))
]


@contextmanager
def virtualenv():
    with prefix('source ' + os.path.join(Environment.get('SERVER_VENV'), 'bin/activate')):
        yield


@task
def restart():
    sudo('supervisorctl restart rhodes')
    sudo('service nginx restart')

@task
def pip():
    with cd(Environment.get('SERVER_PROJECT_DIR')):
        with virtualenv():
            run('pip install -r requirements.txt')


@task
def branch(name):
    switch_branch_command = 'git checkout {branch}'.format(branch=name)
    with cd(Environment.get('SERVER_PROJECT_DIR')):
        run('git reset --hard')
        run(switch_branch_command)
        run('git pull')


@task
def migrate():

    lib_dir = os.path.join(Environment.get('SERVER_PROJECT_DIR'), 'application/lib')
    with cd(lib_dir):
        with virtualenv():
            run('alembic revision --autogenerate')
            run('alembic upgrade head')


@task
def setup():
    pass


@task
def deploy():
    branch('master')
    pip()
    restart()

