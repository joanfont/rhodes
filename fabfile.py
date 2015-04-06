from fabric.context_managers import cd
from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.state import env

from config.prod import rhodes as prod_config


env.hosts = ['rhodes.joan-font.com']
env.user = 'root'

@task
def restart():
    sudo('supervisorctl restart rhodes')
    sudo('service nginx restart')


@task
def setup():
    pass


@task
def deploy():

    with cd(prod_config.PROJECT_DIR):
        run('git reset --hard')
        run('git co master')
        run('git pull')

    restart()

