from fabric.api import *

env.user = 'djvercereg'
env.hosts = ['escience8.inf.ed.ac.uk',]

def prepare_deployment():
  local('python manage.py test')
  local('git add -p && git commit')
  # local('git checkout master && git merge ' + branch_name)

def deploy():
  with lcd('/path/to/my/prod/area/'):
    run('git pull /my/path/to/dev/area/')
    run('python manage.py migrate')
    run('python manage.py test')
    run('/usr/sbin/service apache2 restart')
