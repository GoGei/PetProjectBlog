import os
import random

from fabric.api import local, lcd
from fabric.contrib import django
from fabric.decorators import task

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/'

django.project('blog')
django.settings_module('config.local_settings')


def _launch_django(project_path):
    summ = sum([ord(char) for char in project_path.split('/')[-2]])
    random.seed(summ)
    port = random.randrange(1024, 5000)

    server_address = '127.0.0.1'
    if os.path.exists('/etc/hosts'):
        with open('/etc/hosts') as f:
            if f.read().find('blog.local') != -1:
                server_address = 'blog.local'

    with lcd(project_path):
        local('./manage.py runserver %s:%d' % (
            server_address,
            port), capture=False)


@task
def runserver():
    _launch_django(PROJECT_ROOT)
