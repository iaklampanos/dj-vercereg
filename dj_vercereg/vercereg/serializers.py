from django.contrib.auth.models import User, Group
from models import WorkspaceItem, Workspace, PESig, FunctionSig, LiteralSig, PEImplementation, FnImplementation, RegistryUserGroup
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.reverse import reverse

class UserSerializer(serializers.HyperlinkedModelSerializer):  
  def restore_object(self, attrs, instance=None):
    user = super(UserSerializer, self).restore_object(attrs, instance)
    user.set_password(attrs['password'])
    return user

  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', 'last_name', 'password', 'groups')
    write_only_fields = ('password',)

class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', 'last_name', 'password', 'groups')
    write_only_fields = ('password',)
    read_only_fields = ('username',)
  
  def restore_object(self, attrs, instance=None):
    user = super(UserUpdateSerializer, self).restore_object(attrs, instance)
    user.set_password(attrs['password'])
    return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
  group_name = serializers.CharField(source='get_group_name', read_only=True)
  owner_username = serializers.CharField(source='get_owner_username', read_only=True)
  class Meta:
    model = RegistryUserGroup
    fields = ('group_name', 'owner_username', 'group', 'owner', )


class PEImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PEImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'workspace')


class FnImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FnImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'workspace')


class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Workspace
    depth = 0
    read_only_fields = ('owner', 'creation_date',)


class WorkspaceDeepSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Workspace
    depth = 1
    read_only_fields = ('owner', 'creation_date')
  
  # def transform_owner(self, obj, value):
  #   ser = UserSerializer(value)
  #   print 'data: ', str(ser.data)
  #   return ser.data


class PESigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PESig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'description')

class FunctionSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FunctionSig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'description')

class LiteralSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = LiteralSig
    fields = ('id', 'workspace', 'pckg', 'name', 'value',)
