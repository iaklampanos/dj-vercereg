from django.contrib.auth.models import User, Group
from models import WorkspaceItem, Workspace, PESig, FunctionSig, LiteralSig, PEImplementation, FnImplementation, RegistryUserGroup
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import serializers
from vercereg.utils import get_base_rest_uri

##############################################################################
class UserSerializer(serializers.HyperlinkedModelSerializer):
  groups = serializers.SerializerMethodField('get_reg_groups')

  def get_reg_groups(self, obj):
    toret = []
    # print '>> ', str(obj.groups)
    request = self.context.get('request')
    for v in obj.groups.values():
      # FIXME: Constructs the URL manually, via the request, which is not advisable (insecure and not very robust)
      group_id = v['id']
      g = Group.objects.get(id=group_id)
      rug_instance = RegistryUserGroup.objects.get(group=g)
      rug = get_base_rest_uri(request) + 'registryusergroups/' + str(rug_instance.id) + '/'
      toret.append(rug)
    return toret

  def restore_object(self, attrs, instance=None):
    user = super(UserSerializer, self).restore_object(attrs, instance)
    user.set_password(attrs['password'])
    return user

  class Meta:
    model = User
    fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'groups', 'owns')
    write_only_fields = ('password',)
    read_only_fields = ('owns',)

##############################################################################
class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'email', 'first_name', 'last_name', 'password', 'groups', 'owns')
    write_only_fields = ('password',)
    read_only_fields = ('username',)
  
  def restore_object(self, attrs, instance=None):
    user = super(UserUpdateSerializer, self).restore_object(attrs, instance)
    user.set_password(attrs['password'])
    return user

##############################################################################
class RegistryUserGroupSerializer(serializers.HyperlinkedModelSerializer):
  group_name = serializers.CharField(source='get_group_name')#, read_only=True)
  owner_username = serializers.CharField(source='get_owner_username', read_only=True)

  class Meta:
    model = RegistryUserGroup
    fields = ('url', 'group_name', 'owner_username', 'group', 'owner', 'description')
    read_only_fields = ('group', 'owner')

##############################################################################
class AdminRegistryUserGroupSerializer(serializers.HyperlinkedModelSerializer):
  group_name = serializers.CharField(source='get_group_name')#, read_only=True)
  owner_username = serializers.CharField(source='get_owner_username', read_only=True)

  class Meta:
    model = RegistryUserGroup
    fields = ('url', 'group_name', 'owner_username', 'group', 'owner', 'description')
    read_only_fields = ('group', )


##############################################################################
class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('name',)

##############################################################################
class PEImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PEImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'workspace')

##############################################################################
class FnImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FnImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'workspace')

##############################################################################
class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Workspace
    depth = 0
    read_only_fields = ('owner', 'creation_date',)

##############################################################################
class WorkspaceDeepSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Workspace
    # TODO (nice-to-have) revisit the depth issue, user serialization is not good enough - disabled for now. 
    depth = 0
    read_only_fields = ('owner', 'creation_date')
  
  # def transform_owner(self, obj, value):
  #   ser = UserSerializer(value)
  #   print 'data: ', str(ser.data)
  #   return ser.data

##############################################################################
class PESigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PESig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'description')

##############################################################################
class FunctionSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FunctionSig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'description')

##############################################################################
class LiteralSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = LiteralSig
    fields = ('id', 'workspace', 'pckg', 'name', 'value',)
