from fabric.api import *

env.user = 'djvercereg'
env.hosts = ['escience8.inf.ed.ac.uk',]
env.project_root = '/var/www/vercereg/dj_vercereg'

def prepare_deployment():
  local('python manage.py test')
  local('git add -p && git commit')
  # local('git checkout master && git merge ' + branch_name)

def deploy():
  with cd(env.project_root):
    run('./manage.py collectstatic -v0 --noinput')
