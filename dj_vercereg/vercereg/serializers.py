from django.contrib.auth.models import User, Group
from models import WorkspaceItem, Workspace, PESig, FunctionSig, LiteralSig, PEImplementation, FnImplementation, RegistryUserGroup, Connection, FunctionParameter
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
    read_only_fields = ('user', 'creation_date',)

##############################################################################
class FnImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FnImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'workspace')
    read_only_fields = ('user', 'creation_date',)

##############################################################################
class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Workspace
    depth = 0
    fields = ('id', 'url', 'name', 'owner', 'description', 'creation_date')
    read_only_fields = ('owner', 'creation_date',)

##############################################################################
class WorkspaceDeepSerializer(serializers.HyperlinkedModelSerializer):
  
  pes = serializers.CharField(source='get_pesigs')
  functions = serializers.CharField(source='get_fnsigs')
  literals = serializers.CharField(source='get_literalsigs')
  peimplementations = serializers.CharField(source='get_peimplementations')
  fnimplementations = serializers.CharField(source='get_fnimplementations')
  
  class Meta:
    model = Workspace
    # TODO (nice-to-have) revisit the depth issue, user serialization is not good enough - disabled for now. 
    depth = 0
    read_only_fields = ('owner', 'creation_date')
  
  def transform_pes(self, obj, value):
    request = self.context.get('request')
    pes = obj.pesig_set.get_queryset()
    return map(lambda p: get_base_rest_uri(request) + 'pes/' + str(p.id), pes)

  def transform_functions(self, obj, value):
    request = self.context.get('request')
    fns = obj.functionsig_set.get_queryset()
    return map(lambda p: get_base_rest_uri(request) + 'functions/' + str(p.id), fns)

  def transform_literals(self, obj, value):
    request = self.context.get('request')
    lits = obj.literalsig_set.get_queryset()
    return map(lambda p: get_base_rest_uri(request) + 'literals/' + str(p.id), lits)
  
  def transform_peimplementations(self, obj, value):
    request = self.context.get('request')
    peimpls = obj.peimplementation_set.get_queryset()
    return map(lambda p: get_base_rest_uri(request) + 'peimpls/' + str(p.id), peimpls)
  
  def transform_fnimplementations(self, obj, value):
    request = self.context.get('request')
    fnimpls = obj.fnimplementation_set.get_queryset()
    return map(lambda p: get_base_rest_uri(request) + 'fnimpls/' + str(p.id), fnimpls)


##############################################################################
class PESigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PESig
    fields = ('url', 'id', 'workspace', 'pckg', 'name', 'user', 'description', 'connections', 'creation_date', )
    read_only_fields = ('user', 'creation_date',)

##############################################################################
class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Connection

class FunctionParameterSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FunctionParameter

##############################################################################
class FunctionSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FunctionSig
    fields = ('url', 'id', 'workspace', 'pckg', 'name', 'user', 'description', 'creation_date', 'return_type', 'parameters')
    read_only_fields = ('user', 'creation_date', )

##############################################################################
class LiteralSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = LiteralSig
    fields = ('url', 'id', 'workspace', 'pckg', 'name', 'value', 'description', 'creation_date', )
    read_only_fields = ('user', 'creation_date', )
