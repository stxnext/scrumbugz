from __future__ import with_statement
from fabric.api import *
from fabric.operations import put
from fabric.contrib import files
import os
import string

def raphael():
    """
    DEVELOPMENT
    """
    env.hosts = ['krotkiewicz@raphael.stxnext.pl',]
    env.directory = '~/scrumbugz'

def reload_supervisord():
    run('./bin/supervisorctl -c parts/etc/supervisord.conf update')
    run('./bin/supervisorctl -c parts/etc/supervisord.conf restart all')

def start_supervisord():
     with cd(env.directory):
         run('./bin/supervisord -c parts/etc/supervisord.conf')

def db_migrate():
    run('./bin/manage migrate --noinput')

def collect_static():
    run('./bin/manage collectstatic --noinput')

def buildout():
    run('./bin/buildout -vNc production.cfg')

def upgrade(branch=None):
    with cd(env.directory):
        if branch:
            run('git remote update')
            run('git checkout %s' % branch)
        run('git pull')
        buildout()
        db_migrate()
        collect_static()
        reload_supervisord()
