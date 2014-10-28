from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from vercereg.separated_values_field import SeparatedValuesField
import reversion

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        

class Workspace(models.Model):
  '''
  The workspace entity. A workspace is designed so that it provides an independent sandbox for storing and working with various kinds of workspace items and related entities. A workspace is identified by the user+name.
  '''
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(User)
  # group = models.ForeignKey(Group)
  description = models.TextField(null=True, blank=True)
  unique_together = (("owner", "name"),)

  def __unicode__(self):
    return u'%s: %s' % (self.owner.username, self.name)

  def get_workspace_items(self):
    print '(get_workspace_items)'
    print str(self.genericsig_set)
    return self.genericsig_set
  
  def get_pesigs(self):
    print self.workspaceitem_set
    
  class Meta:
    verbose_name = 'workspace'
    permissions = (
      ('view_meta_workspace', 'Can view the workspace in a list.'),
      ('view_contents_workspace', 'Can view the contents of a workspace and clone it.'),
      ('modify_meta_workspace', 'Can modify the metadata of a workspace.'),
      ('modify_contents_workspace', 'Can alter the contents of a workspace.'),
    )


class WorkspaceItem(models.Model):
  '''
  An abstract model representing the basis for concrete workspace items, such as functions and PEs. A workspace item has at least a package, a name, a user and a user-group. Each workspace item belongs to exactly one workspace.
  '''
  workspace = models.ForeignKey(Workspace)
  pckg = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  user = models.ForeignKey(User)
  # group = models.ForeignKey(Group)

  class Meta:
    abstract = True
    
  def __unicode__(self):
    return u'[%s] %s.%s' % (self.workspace, self.pckg, self.name)


class PESig(WorkspaceItem):
  '''
  A model representing the signature of a PE. PEs are workspace items.
  '''
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  # Implied connection_set fields due to ForeignKey in Connection relation
  PE_TYPES = (
    ('ABSTRACT', 'Abstract'),
    ('PRIMITIVE', 'Primitive'),
    ('COMPOSITE', 'Composite')
  )

  kind = models.CharField(max_length=10, choices=PE_TYPES)
  
  class Meta:
    verbose_name = "PE"
    verbose_name_plural = "PEs"


class Connection(models.Model):
  '''
  A model representing a PE connections. Connections are descriptions of pipes between PEs and belong to their respective PEs. As they are not designed to be dealt with independently of their PEs, connections are not workspace items.
  '''
  CONNECTION_TYPES = (
    ('IN', 'In'),
    ('OUT', 'Out')
  )

  kind = models.CharField(max_length=3, choices=CONNECTION_TYPES)
  name = models.CharField(max_length=30)
  s_type = models.CharField(max_length=30, null=True, blank=True)
  d_type = models.CharField(max_length=30, null=True, blank=True)
  comment = models.CharField(max_length=200, null=True, blank=True)
  is_array = models.BooleanField(default=False)
  pesig = models.ForeignKey(PESig)
  modifiers = SeparatedValuesField(null=True, blank=True)

  def __unicode__(self):
    return u'[%s] %s (%s|%s)' % (self.pesig, self.name, self.kind, self.modifiers)


class LiteralSig(WorkspaceItem):
  '''
  A model representing a literal in a workspace. Literals only carry a package.name and a value. They are workspace items.
  '''
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  value = models.CharField(max_length=50, null=True, blank=False)

  class Meta:
    verbose_name = "literal"


class FunctionSig(WorkspaceItem):
  '''
  A model representing a function in a workspace. 
  '''
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  return_type = models.CharField(max_length=30)
  
  class Meta:
    verbose_name = "function"


class FunctionParameters(models.Model):
  '''
  A model representing a tuple of function parameters. Similar to connections, parameters only exist within their parent functions, they are therefore not made to be workspace items - these are their owning functions. 
  '''
  param_name = models.CharField(max_length=30)
  param_type = models.CharField(max_length=30, null=True, blank=True, default=None)
  parent_function = models.ForeignKey(FunctionSig)
  

class WorkflowSig(WorkspaceItem):
  '''
  A workflow signature model, to hold information about whole workflows.
  TODO: Think about implementation. 
  '''
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  
  class Meta:
    verbose_name = "workflow"


class PEImplementation(WorkspaceItem):
  '''
  This is a model to hold an implementation of a PE. This is a separate workspace item and it will be associated to exactly one PESig (many-to-one).
  '''
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(PESig)
  
  def short_code(self):
    return self.code[0:35] + ' [...]'
  
  class Meta:
    verbose_name = "PE implementation"


class FnImplementation(WorkspaceItem):
  '''
  A model to encapsulate the notion of a function implementation. This is a workspace item and it is associated to exactly one FunctionSig instance (many-to-one).
  '''
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(FunctionSig)
  
  def short_code(self):
    return self.code[0:35] + ' [...]'
    
  class Meta:
    verbose_name = "function implementation"
    

# Reversion registrations for version control
reversion.register(Workspace)
reversion.register(WorkspaceItem)
reversion.register(PESig)
reversion.register(Connection)
reversion.register(FunctionSig)
reversion.register(FunctionParameters)
reversion.register(LiteralSig)
reversion.register(WorkflowSig)
reversion.register(PEImplementation)
reversion.register(FnImplementation)