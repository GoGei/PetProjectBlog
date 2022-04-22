import os
import random
from datetime import datetime

from fabric.api import local, lcd, cd
from fabric.contrib import django
from fabric.decorators import task

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/'

django.project('blog')
django.settings_module('config.local_settings')
from config import local_settings as dj_settings


def _launch_django(project_path):
    port = dj_settings.HOST_PORT
    if not port:
        summ = sum([ord(char) for char in project_path.split('/')[-2]])
        random.seed(summ)
        port = random.randrange(1024, 5000)

    server_address = '127.0.0.1'
    if os.path.exists('/etc/hosts'):
        with open('/etc/hosts') as f:
            if f.read().find(dj_settings.SITE_URL) != -1:
                server_address = dj_settings.SITE_URL

    with lcd(project_path):
        local('./manage.py runserver %s:%s' % (
            server_address,
            port), capture=False)


@task
def runserver():
    _launch_django(PROJECT_ROOT)


@task
def dump_db():
    user = 'postgres'
    db_name = dj_settings.DATABASES['default']['NAME']

    date = datetime.now().strftime("%Y-%m-%d_%H%M")
    dump_name = f'dumps/{db_name}_{date}.sql'
    dump_zip_name = dump_name+'.bz2'

    with cd(PROJECT_ROOT):
        local('mkdir -p dumps')
        local(f'sudo -u {user} pg_dump {db_name} > {dump_name} | bzip2 -9 > {dump_zip_name}')


@task
def deploy_local(branch=None):
    branch = branch or 'main'

    local('git checkout %s && git pull' % branch)
    local('pip3 install -r requirements.txt')
    local('./manage.py migrate')
    local('./manage.py collectstatic --noinput')
