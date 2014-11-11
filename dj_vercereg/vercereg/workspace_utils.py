from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import LiteralSig
from vercereg.models import PEImplementation
from vercereg.models import PESig
from vercereg.models import Workspace
from vercereg.models import RegistryUserGroup
from vercereg.models import Connection

from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.utils import timezone

# from django.db import transaction


class WorkspaceCloner:
  '''Implements a deep cloner for vercereg workspaces.'''
  
  def __init__(self, original_workspace, name, user):
    self.original_workspace = original_workspace
    self.target_workspace = None
    self.name = name
    self.user = user
    self.dic = {} # dictionary fromWorkspaceItem:toWorkspaceItem, when cloned
  
  def clone_pe(self, pe):
    if pe in self.dic: return self.dic[pe]
    ret = PESig()
    ret.description = pe.description
    ret.kind = pe.kind
    ret.workspace = self.target_workspace
    ret.pckg = pe.pckg
    ret.name = pe.name
    ret.creation_date = timezone.now() # Update the creation date/time;
    for c in pe.connections:
      newconn = Connection()
      newconn.kind = c.kind
      newconn.name = c.name
      newconn.s_type = c.s_type
      newconn.d_type = c.d_type
      newconn.comment = c.comment
      newconn.is_array = c.is_array
      newconn.modifiers = c.modifiers
      newconn.pesig = ret
    for p in pe.peimplementation_set:
      newp = self.clone_peimpl(p) # foreign key doesn't need to be updated here
    ret.save()
    self.dic[pe] = ret
    return ret
    
  def clone_literal(self, lit):
    if lit in self.dic: return self.dic[lit]
    ret = LiteralSig()
    ret.workspace = self.target_workspace
    ret.pckg = lit.pckg
    ret.name = lit.name
    ret.creation_date = timezone.now()
    ret.description = lit.description
    ret.value = lit.value
    ret.save()
    self.dic[lit] = ret
    return ret
  
  def clone_function(self, fun):
    pass
  
  def clone_peimpl(self, peimpl):
    pass
  
  def clone_fnimpl(self, fnimpl):
    pass
  

  def clone(self):
    '''Deep clone the original workspace into the target and return it.'''
    print 'Cloning ' + str(self.original_workspace)
    self.target_workspace = Workspace(name=self.name, owner=self.user, creation_date=timezone.now(), description=self.original_workspace.description)
    self.target_workspace.save()
    
    for pe in self.original_workspace.get_pesigs():
      self.dic[pe] = self.clone_pe(pe)
    
    for lit in self.original_workspace.get_literalsigs():
      self.dic[lit] = self.clone_literal(lit)
    
    for fn in self.original_workspace.get_fnsigs():
      self.dic[fn] = self.clone_function(fn)
    
    for peimpl in self.original_workspace.get_peimplementations():
      self.dic[peimpl] = self.clone_peimpl(peimpl)
    
    for fnimpl in self.original_workspace.get_fnimplementations():
      self.dic[fnimpl] = self.clone_fnimpl(fnimpl)
    
    return None