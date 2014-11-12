from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import FunctionParameter
from vercereg.models import LiteralSig
from vercereg.models import PEImplementation
from vercereg.models import PESig
from vercereg.models import Workspace
from vercereg.models import RegistryUserGroup
from vercereg.models import Connection

from django.utils import timezone


# Silly counter to be used for named differentiation
COUNTER=1000
def next_no():
  COUNTER += 1
  return str(COUNTER)

############!!!#############
# bob is the default user. # 
############################

def create_ref_user(username='bob'):
  return User.objects.create(username=username)

def create_ref_workspace(owner=None, name=None):
  if not owner: owner = create_ref_user()
  if not name: name = owner.username + '_wspc'
  return Workspace.objects.create(name=name, owner=owner, description='Description of reference workspace %s'%(name), creation_date=timezone.now())

def create_ref_conn(pe, name='some_connection', kind='In'):
  return Connection.objects.create(name=name, kind=kind, pesig=pe)

def create_ref_pe(workspace=None, name=None, user=None, pckg='pes', kind='Abstract'):
  if not user: user = User.objects.get(username='bob')
  if not workspace: workspace = Workspace.objects.get(name='bob_wspc')
  if not name: name = user.username + '_pe_' + next_no()
  return PESig.objects.create(workspace=workspace, pckg=pckg, name=name, kind=kind)

def create_ref_fn_param(fn, param_name='fn_param', param_type='T'):
  return FunctionParameter.objects.create(parent_function=fn, param_type:param_type, param_name:param_name)

def create_ref_fn(workspace=None, name=None, user=None, pckg='fns', return_type='RTYPE'):
  if not user: user = User.objects.get(username='bob')
  if not workspace: workspace = Workspace.objects.get(name='bob_wspc')
  if not name: name = user.username + '_pe_' + next_no()
  FunctionSig.objects.create(workspace=workspace, user=user, pckg=pckg, name=name, return_type=return_type)
  
# TODO: Implement tests for workspaces. 
def create_ref_peimpl():
  pass
def create_ref_fnimpl():
  pass

class DefaultValuesTestCase(TestCase):
  fixtures = ['fixtures/def_group.json',]
  
  def test_read_all_group_exists(self):
    g = Group.objects.all().get(name='default_read_all_group')
    self.assertIsNotNone(g)

  def test_read_all_rug(self):
    g = Group.objects.all().get(name='default_read_all_group')
    rug = RegistryUserGroup.objects.all().get(group=g)
    self.assertIsNotNone(rug)


# TODO: Implement the workspace test case
class WorkspaceTestCase(TestCase):
  
  def setUp(self):
    bob = create_ref_user('bob')
    pat = create_ref_user('pat')
    bob_wspc = create_ref_workspace(owner=bob)
    pat_wspc = create_ref_workspace(owner=pat)
  
  def test_workspace_create(self):
    assert Workspace.objects.get(name='bob_wspc').name == 'bob_wspc'
  
  def test_user_create(self):
    assert len(User.objects.all()) == 3 # 2 for pat, bob + 1 for anonymous
  
  def test_workspace_cloning(self):
    pass
    
