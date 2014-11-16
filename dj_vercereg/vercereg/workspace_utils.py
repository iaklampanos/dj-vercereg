from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import FunctionParameter
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
    ret.user = self.user
    ret.save() # Initial save
    for c in pe.connections.all():
      newconn = Connection()
      newconn.kind = c.kind
      newconn.name = c.name
      newconn.s_type = c.s_type
      newconn.d_type = c.d_type
      newconn.comment = c.comment
      newconn.is_array = c.is_array
      newconn.modifiers = c.modifiers
      newconn.pesig = ret
      newconn.save()
    for p in pe.peimplementation_set.all():
      newp = self.clone_peimpl(p, ret) # foreign key doesn't need to be updated here
    
    # ret.save() # Update FIXME: Probably not needed...
    self.dic[pe] = ret
    return ret

  def clone_peimpl(self, peimpl, newparent=None):
    if peimpl in self.dic: return self.dic[peimpl]
    ret = PEImplementation()
    ret.workspace = self.target_workspace
    ret.pckg = peimpl.pckg
    ret.name = peimpl.name
    ret.creation_date = timezone.now()
    ret.description = peimpl.description
    ret.code = peimpl.code
    ret.user = self.user
    if newparent: ret.parent_sig = newparent
    
    ret.save()
    self.dic[peimpl] = ret
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
    ret.user = self.user
    
    ret.save()
    self.dic[lit] = ret
    return ret
  
  def clone_function(self, fun):
    if fun in self.dic: return self.dic[fun]
    ret = FunctionSig()
    ret.workspace = self.target_workspace
    ret.pckg = fun.pckg
    ret.name = fun.name
    ret.creation_date = timezone.now()
    ret.description = fun.description
    ret.return_type = fun.return_type
    ret.user = self.user
    
    ret.save()
    for param in fun.parameters.all():
      newparam = FunctionParameter()
      newparam.param_name = param.param_name
      newparam.param_type = param.param_type
      newparam.parent_function = ret
      newparam.save()
    for fnimpl in fun.fnimplementation_set.all():
      newf = self.clone_fnimpl(fnimpl, ret)
    
    #ret.save()
    self.dic[fun] = ret
    return ret
  
  def clone_fnimpl(self, fnimpl, newparent=None):
    if fnimpl in self.dic: return self.dic[fnimpl]
    ret = FnImplementation()
    ret.workspace = self.target_workspace
    ret.pckg = fnimpl.pckg
    ret.name = fnimpl.name
    ret.creation_date = timezone.now()
    ret.description = fnimpl.description
    ret.code = fnimpl.code
    if newparent: ret.parent_sig = newparent
    ret.user = self.user
    
    ret.save()
    self.dic[fnimpl] = ret
    return ret
  

  def clone(self):
    '''Deep clone the original workspace into the target and return it.'''
    # print 'Cloning ' + str(self.original_workspace)
    
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
    
    return self.target_workspace