# Copyright 2014 The University of Edinburgh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from vercereg.separated_values_field import SeparatedValuesField
import reversion
import datetime
from vercereg.utils import get_base_rest_uri

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#   if created:
#     Token.objects.create(user=instance)


class RegistryUserGroup(models.Model):
  '''Extends the group model so that it incorporates owner-users.'''
  group = models.OneToOneField(Group)
  owner = models.ForeignKey(User, related_name='owns')
  description = models.TextField(null=True, blank=True)

  def get_group_name(self):
    return self.group.name

  def get_owner_username(self):
    return self.owner.username


class Workspace(models.Model):
  ''' The workspace entity. A workspace is designed so that it provides an independent sandbox for storing and working with various kinds of workspace items and related entities. A workspace is identified by the user+name. '''

  name = models.CharField(max_length=100, null=False, blank=False)
  owner = models.ForeignKey(User)
  description = models.TextField(null=True, blank=True)
  unique_together = (("owner", "name"),)
  creation_date = models.DateTimeField(default=datetime.datetime.now())

  def __unicode__(self):
    return u'%s: %s' % (self.owner.username, self.name)

  def get_pesigs(self):
    return self.pesig_set.get_queryset()

  def get_fnsigs(self):
    return self.functionsig_set.get_queryset()

  def get_literalsigs(self):
    return self.literalsig_set.get_queryset()

  def get_peimplementations(self):
    return self.peimplementation_set.get_queryset()

  def get_fnimplementations(self):
    return self.fnimplementation_set.get_queryset()

  class Meta:
    verbose_name = 'workspace'
    permissions = (
      ('view_meta_workspace', 'Can view the workspace in a list.'),
      ('view_contents_workspace', 'Can view the contents of a workspace and clone it.'),
      ('modify_meta_workspace', 'Can modify the metadata of a workspace.'),
      ('modify_contents_workspace', 'Can alter the contents of a workspace.'),
    )

# TODO: Move creation_time to WorkspaceItems
# TODO: Add modification_time to WorkspaceItems
class WorkspaceItem(models.Model):
  '''
  An abstract model representing the basis for concrete workspace items, such as functions and PEs. A workspace item has at least a package, a name, a user and a user-group. Each workspace item belongs to exactly one workspace.
  '''
  workspace = models.ForeignKey(Workspace)
  pckg = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  user = models.ForeignKey(User)
  # group = models.ForeignKey(Group)
  creation_date = models.DateTimeField()
  
  class Meta:
    abstract = True
    unique_together = ('workspace', 'pckg', 'name', )

  def __unicode__(self):
    return u'[%s] %s.%s' % (self.workspace, self.pckg, self.name)


class PESig(WorkspaceItem):
  '''
  A model representing the signature of a PE. PEs are workspace items.
  '''
  description = models.TextField(null=True, blank=True)
  # Implied connection_set fields due to ForeignKey in Connection relation
  PE_TYPES = (
    ('ABSTRACT', 'Abstract'),
    ('PRIMITIVE', 'Primitive'),
    ('COMPOSITE', 'Composite')
  )

  kind = models.CharField(max_length=10, choices=PE_TYPES)

  def _get_full_name(self):
    return '%s.%s' % (self.pckg, self.name)
  full_name = property(_get_full_name)

  class Meta:
    verbose_name = "PE"
    verbose_name_plural = "PEs"
    unique_together = ('workspace', 'pckg', 'name')


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
  pesig = models.ForeignKey(PESig, related_name='connections')
  modifiers = SeparatedValuesField(null=True, blank=True)

  def __unicode__(self):
    return u'[%s] %s (%s|%s)' % (self.pesig, self.name, self.kind, self.modifiers)


class LiteralSig(WorkspaceItem):
  '''
  A model representing a literal in a workspace. Literals only carry a package.name and a value. They are workspace items.
  '''
  description = models.TextField(null=True, blank=True)
  value = models.CharField(max_length=50, null=True, blank=False)
  def _get_full_name(self):
    return '%s.%s' % (self.pckg, self.name)
  full_name = property(_get_full_name)

  class Meta:
    verbose_name = "literal"
    unique_together = ('workspace', 'pckg', 'name')


class FunctionSig(WorkspaceItem):
  '''
  A model representing a function in a workspace.
  '''
  description = models.TextField(null=True, blank=True)
  return_type = models.CharField(max_length=30)
  def _get_full_name(self):
    return '%s.%s' % (self.pckg, self.name)
  full_name = property(_get_full_name)

  class Meta:
    verbose_name = "function"
    unique_together = ('workspace', 'pckg', 'name')


class FunctionParameter(models.Model):
  '''
  A model representing a tuple of function parameters. Similar to connections, parameters only exist within their parent functions, they are therefore not made to be workspace items - these are their owning functions.
  '''
  param_name = models.CharField(max_length=30)
  param_type = models.CharField(max_length=30, null=True, blank=True, default=None)
  parent_function = models.ForeignKey(FunctionSig, related_name='parameters')


class WorkflowSig(WorkspaceItem):
  '''
  A workflow signature model, to hold information about whole workflows.
  TODO: (nice-to-have) Think about implementation.
  '''
  description = models.TextField(null=True, blank=True)
  def _get_full_name(self):
    return '%s.%s' % (self.pckg, self.name)
  full_name = property(_get_full_name)

  class Meta:
    verbose_name = "workflow"
    unique_together = ('workspace', 'pckg', 'name')


class PEImplementation(WorkspaceItem):
  '''
  This is a model to hold an implementation of a PE. This is a separate workspace item and it will be associated to exactly one PESig (many-to-one).
  '''
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(PESig)
  def _get_full_name(self):
    return '%s.%s' % (self.pckg, self.name)
  full_name = property(_get_full_name)

  def short_code(self):
    return self.code[0:35] + ' [...]'

  class Meta:
    verbose_name = "PE implementation"
    unique_together = ('workspace', 'pckg', 'name')


class FnImplementation(WorkspaceItem):
  '''
  A model to encapsulate the notion of a function implementation. This is a workspace item and it is associated to exactly one FunctionSig instance (many-to-one).
  '''
  description = models.TextField(null=True, blank=True)
  code = models.TextField(null=False, blank=True)
  parent_sig = models.ForeignKey(FunctionSig)
  def _get_full_name(self):
    return '%s.%s' % (self.pckg, self.name)
  full_name = property(_get_full_name)

  def short_code(self):
    return self.code[0:35] + ' [...]'

  class Meta:
    verbose_name = "function implementation"
    unique_together = ('workspace', 'pckg', 'name')


# Reversion registrations for version control
reversion.register(Workspace)
reversion.register(WorkspaceItem)
reversion.register(PESig)
reversion.register(Connection)
reversion.register(FunctionSig)
reversion.register(FunctionParameter)
reversion.register(LiteralSig)
reversion.register(WorkflowSig)
reversion.register(PEImplementation)
reversion.register(FnImplementation)
