from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class Workspace(models.Model):
  name = models.CharField(max_length=100)
  owner = models.ForeignKey(User)
  group = models.ForeignKey(Group)
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

class WorkspaceItem(models.Model):
  workspace = models.ForeignKey(Workspace)
  pckg = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  user = models.ForeignKey(User)
  group = models.ForeignKey(Group)

  class Meta:
    abstract = True
    
  def __unicode__(self):
    return u'[%s] %s.%s' % (self.workspace, self.pckg, self.name)


class PESig(WorkspaceItem):
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

  # ForeignKey in Modifier would imply that there is a modifier_set accessible from Connection

class Modifier(models.Model):
  value = models.CharField(max_length=30)
  connection = models.ForeignKey(Connection)


class LiteralSig(WorkspaceItem):
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  value = models.CharField(max_length=50, null=True, blank=False)

  class Meta:
    verbose_name = "literal"

class FunctionSig(WorkspaceItem):
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  return_type = models.CharField(max_length=30)
  
  class Meta:
    verbose_name = "function"
  
class FunctionParameters(models.Model):
  param_name = models.CharField(max_length=30)
  param_type = models.CharField(max_length=30, null=True, blank=True, default=None)
  parent_function = models.ForeignKey(FunctionSig)
  

class WorkflowSig(WorkspaceItem):
  description = models.TextField(null=True, blank=True)
  creation_date = models.DateTimeField()
  
  class Meta:
    verbose_name = "workflow"

class PEImplementation(WorkspaceItem):
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(PESig)
  
  def short_code(self):
    return self.code[0:35] + ' [...]'
  
  class Meta:
    verbose_name = "PE implementation"

class FnImplementation(WorkspaceItem):
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(FunctionSig)
  
  def short_code(self):
    return self.code[0:35] + ' [...]'
    
  class Meta:
    verbose_name = "function implementation"