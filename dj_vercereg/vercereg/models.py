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
  unique_together = (("owner", "name"),)

  def __unicode__(self):
    return u'%s: %s' % (self.owner.username, self.name)

  def get_workspace_items(self):
    print '(get_workspace_items)'
    print str(self.genericsig_set)
    print str(self.genericdef_set)
    return self.genericsig_set
  
  def get_pesigs(self):
    print self.workspaceitem_set

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


class GenericDef(WorkspaceItem):
  gendef_description = models.CharField(max_length=200)
  creation_date = models.DateTimeField()


class GenericSig(WorkspaceItem):
  gensig_description = models.CharField(max_length=200)
  creation_date = models.DateTimeField()
  gendef = models.ForeignKey(GenericDef)

  # class Meta:
  #   abstract = True


class PESig(GenericSig):
  # Implied connection_set fields due to ForeignKey in Connection relation
  PE_TYPES = (
    ('ABSTRACT', 'Abstract'),
    ('PRIMITIVE', 'Primitive'),
    ('COMPOSITE', 'Composite')
  )

  kind = models.CharField(max_length=10, choices=PE_TYPES)


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


class LiteralSig(GenericSig):
  value = models.CharField(max_length=50, null=True, blank=False)


class Implementation(WorkspaceItem):
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(GenericSig)
  
  def short_code(self):
    return self.code[0:35] + ' [...]'

class FunctionSig(GenericSig):
  return_type = models.CharField(max_length=30)
  
  
class FunctionParameters(models.Model):
  param_name = models.CharField(max_length=30)
  param_type = models.CharField(max_length=30, null=True, blank=True, default=None)
  parent_function = models.ForeignKey(FunctionSig)
  

class WorkflowSig(GenericSig):
  pass
  