import os
from contextlib import contextmanager

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
    base_path = '/root/.virtualenvs/rhodes/'
    activate = 'source ' + os.path.join(base_path, 'bin/activate')
    postactivate = 'source ' + os.path.join(base_path, 'bin/postactivate')
    code_line = activate + ' && ' + postactivate
    with prefix(code_line):
        yield


@task
def restart():
    sudo('supervisorctl restart rhodes')
    sudo('service nginx restart')

@task
def pip():
    with virtualenv():
        with cd(Environment.get('PROJECT_DIR')):
            run('pip install -r requirements.txt')


@task
def test():
    with virtualenv():
        run('echo $DB_PASS')


@task
def branch(name):
    switch_branch_command = 'git checkout {branch}'.format(branch=name)
    with virtualenv():
        with cd(Environment.get('PROJECT_DIR')):
            run('git reset --hard')
            run(switch_branch_command)
            run('git pull')


@task
def migrate():
    with virtualenv():
        lib_dir = os.path.join(Environment.get('PROJECT_DIR'), 'application/lib')
        with cd(lib_dir):
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

