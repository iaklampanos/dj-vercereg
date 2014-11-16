from django.test import TestCase, RequestFactory, Client

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

from vercereg.views import WorkspaceViewSet
from vercereg.views import UserViewSet

from vercereg.workspace_utils import WorkspaceCloner

from django.utils import timezone

from rest_framework import status


# Silly counter to be used for named differentiation
COUNTER = 1000
def next_no():
  global COUNTER
  COUNTER += 1
  return str(COUNTER)

############!!!#############
# bob is the default user. # 
############################

def create_ref_user(username='bob', password='bob'):
  u = User.objects.create(username=username)
  u.set_password(password)
  u.save()
  return u

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
  return PESig.objects.create(workspace=workspace, user=user, pckg=pckg, name=name, kind=kind, creation_date=timezone.now())

def create_ref_fn_param(fn, param_name='fn_param', param_type='T'):
  return FunctionParameter.objects.create(parent_function=fn, param_type=param_type, param_name=param_name)

def create_ref_fn(workspace=None, name=None, user=None, pckg='fns', return_type='RET_TYPE'):
  if not user: user = User.objects.get(username='bob')
  if not workspace: workspace = Workspace.objects.get(name='bob_wspc')
  if not name: name = user.username + '_pe_' + next_no()
  return FunctionSig.objects.create(workspace=workspace, user=user, pckg=pckg, name=name, return_type=return_type, creation_date=timezone.now())
  
# TODO: Implement tests for workspaces. 
def create_ref_peimpl(pe, name=None, user=None, pckg='peimpls', code='PE Impl Code', description=None):
  if not user: user = User.objects.get(username='bob')
  workspace = pe.workspace
  if not name: name = user.username + '_peimpl_' + next_no()
  if not description: description = name + ' description text.'
  return PEImplementation.objects.create(workspace=workspace, pckg=pckg, name=name, user=user, code=code, description=description, parent_sig=pe, creation_date=timezone.now())
  
def create_ref_fnimpl(fn, name=None, user=None, pckg='fnimpls', code='PE Impl Code', description=None):
  if not user: user = User.objects.get(username='bob')
  workspace = fn.workspace
  if not name: name = user.username + '_fnimpl_' + next_no()
  if not description: description = name + ' description text.'
  return FnImplementation.objects.create(workspace=workspace, pckg=pckg, name=name, user=user, code=code, description=description, parent_sig=fn, creation_date=timezone.now())


class DefaultValuesTestCase(TestCase):
  fixtures = ['fixtures/def_group.json',]
  
  def test_read_all_group_exists(self):
    g = Group.objects.all().get(name='default_read_all_group')
    self.assertIsNotNone(g)

  def test_read_all_rug(self):
    g = Group.objects.all().get(name='default_read_all_group')
    rug = RegistryUserGroup.objects.all().get(group=g)
    self.assertIsNotNone(rug)
    

class AuthorizationTestCase(TestCase):
  fixtures = ['fixtures/def_group.json',]

  def setUp(self):
    self.factory = RequestFactory()
    self.bob = create_ref_user('bob')
    
  def test_log_in(self):
    c = Client()
    response = c.post('/api-token-auth/', {'username':'bob', 'password':'bob'})
    assert response.status_code == status.HTTP_200_OK

# TODO: Implement the workspace test case
class WorkspaceTestCase(TestCase):
  fixtures = ['fixtures/def_group.json',]
  
  def setUp(self):
    # Make some instance vars for easy access
    self.factory = RequestFactory()
    
    self.bob = create_ref_user('bob')
    self.pat = create_ref_user('pat')
    
    # create a couple of workspaces
    self.bob_wspc = create_ref_workspace(owner=self.bob)
    self.pat_wspc = create_ref_workspace(owner=self.pat)
    
    # create a couple PEs in the 1st workspace (default)
    pe1 = create_ref_pe()
    pe2 = create_ref_pe()
    create_ref_conn(pe1, name='alpha')
    create_ref_conn(pe1, name='beta', kind='Out')
    create_ref_conn(pe2, name='gamma')
    create_ref_peimpl(pe1, name='ImplPE1forBOB')
    
    # create a function in the default workspace
    fn = create_ref_fn(workspace=self.bob_wspc)
    create_ref_fn_param(fn)
    create_ref_fnimpl(fn, name="refImplforFunctioninBOB")
  
  def test_workspace_create(self):
    assert Workspace.objects.get(name='bob_wspc').name == 'bob_wspc'
  
  def test_user_create(self):
    assert len(User.objects.all()) == 3 # 2 for pat, bob + 1 for anonymous
  
  def test_workspace_contents(self):
    assert len(PESig.objects.all()) == 2
    w = Workspace.objects.get(name='bob_wspc')
    assert len(w.pesig_set.values()) == 2
    assert len(w.peimplementation_set.values()) == 1
    assert len(w.functionsig_set.values()) == 1
    assert len(w.fnimplementation_set.values()) == 1
    
  def test_workspace_cloning(self):
    w = Workspace.objects.get(name='bob_wspc')
    cloner = WorkspaceCloner(w, 'clone', self.bob)
    cw = cloner.clone()
    
    # Compare counts of workspace items
    assert len(cw.pesig_set.values()) == len(w.pesig_set.values())
    assert len(cw.peimplementation_set.values()) == len(w.peimplementation_set.values())
    assert len(cw.functionsig_set.values()) == len(w.functionsig_set.values())
    assert len(cw.fnimplementation_set.values()) == len(w.fnimplementation_set.values())
    
  
  def test_request_clone_workspace(self):
    c = Client()
    login_result = c.login(username='bob', password='bob')
    self.assertTrue(login_result)
    response = c.post('/rest/workspaces/?clone_of=1', {'name':'bobnewspace'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # check contents:
    w = Workspace.objects.get(id=1)
    cw = Workspace.objects.get(name='bobnewspace')
    self.assertIsNotNone(cw)
    self.assertEqual(cw.name, 'bobnewspace')
    self.assertEqual(cw.id, 3)
    self.assertEqual(len(cw.pesig_set.values()), len(w.pesig_set.values()))
    self.assertEqual(len(cw.peimplementation_set.values()), len(w.peimplementation_set.values()))
    self.assertEqual(len(cw.functionsig_set.values()), len(w.functionsig_set.values()))
    self.assertEqual(len(cw.fnimplementation_set.values()), len(w.fnimplementation_set.values()))
    
    # test internal entities (Connections and FunctionParameters)
    for p1 in list(PESig.objects.filter(workspace=w)):
      p = p1.pckg
      n = p1.name
      # get the corresponding pe in cw 
      p2 = PESig.objects.filter(workspace=cw, pckg=p, name=n)[0]
      self.assertIsNotNone(p2)
      
      conns1 = Connection.objects.filter(pesig=p1)
      conns2 = Connection.objects.filter(pesig=p2)
      self.assertEqual(len(conns1), len(conns2))
    
    for fn1 in list(FunctionSig.objects.filter(workspace=w)):
      p = fn1.pckg
      n = fn1.name
      
      fn2 = FunctionSig.objects.filter(workspace=cw, pckg=p, name=n)[0]
      self.assertIsNotNone(fn2)
      
      params1 = FunctionParameter.objects.filter(parent_function=fn1)
      params2 = FunctionParameter.objects.filter(parent_function=fn2)
      self.assertEqual(len(params1), len(params2))
    