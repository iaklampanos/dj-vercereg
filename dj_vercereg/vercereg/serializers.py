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

# from models import WorkspaceItem
from models import Workspace
from models import PESig
from models import FunctionSig
from models import LiteralSig
from models import PEImplementation
from models import FnImplementation
from models import RegistryUserGroup
from models import Connection
from models import FunctionParameter
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import serializers
from vercereg.utils import get_base_rest_uri

##############################################################################


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def get_reg_groups(self, obj):
        toret = []
        request = self.context.get('request')
        for v in obj.groups.values():
            group_id = v['id']
            g = Group.objects.get(id=group_id)
            try:
                rug_instance = RegistryUserGroup.objects.get(group=g)
                rug = (get_base_rest_uri(request) + 'registryusergroups/' +
                       str(rug_instance.id) + '/')
                toret.append(rug)
            except RegistryUserGroup.DoesNotExist:
                pass
        return toret

    groups = serializers.SerializerMethodField('get_reg_groups')

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'groups',
            'ownsgroups')
        write_only_fields = ('password',)
        read_only_fields = ('ownsgroups',)


# class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
#   groups = serializers.SerializerMethodField('get_reg_groups')
#
#   def get_reg_groups(self, obj):
#     toret = []
#     request = self.context.get('request')
#     for v in obj.groups.values():
#       group_id = v['id']
#       g = Group.objects.get(id=group_id)
#       try:
#         rug_instance = RegistryUserGroup.objects.get(group=g)
#         rug = get_base_rest_uri(request) + 'registryusergroups/' +
#               str(rug_instance.id) + '/'
#         toret.append(rug)
#       except RegistryUserGroup.DoesNotExist:
#         pass
#     return toret
#
#   def restore_object(self, attrs, instance=None):
#     user = super(UserUpdateSerializer, self).restore_object(attrs, instance)
#     user.set_password(attrs['password'])
#     return user
#
#   class Meta:
#     model = User
#     fields = ('username', 'email', 'first_name', 'last_name', 'password',
#               'groups', 'ownsgroups',)
#     write_only_fields = ('password',)
#     read_only_fields = ('username',)

##############################################################################
class RegistryUserGroupSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.CharField(source='get_group_name')
    # FIXME: The following is excluded as it break django rest for some reason.

    class Meta:
        model = RegistryUserGroup
        fields = ('url', 'group_name', 'group', 'owner', 'description', )
        read_only_fields = ('group', 'owner', )


class RegistryUserGroupPutSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.CharField(source='get_group_name')
    # ownerusername = serializers.CharField(source='get_owner_username',
    #                                       read_only=True)

    class Meta:
        model = RegistryUserGroup
        fields = ('url', 'group_name', 'group', 'owner', 'description', )
        read_only_fields = ('group', )

##############################################################################


# class AdminRegistryUserGroupSerializer
#    (serializers.HyperlinkedModelSerializer):
#   group_name = serializers.CharField(source='get_group_name')#,
#                                      read_only=True)
#   owner_username = serializers.CharField(source='get_owner_username',
#                                          read_only=True)
#
#   class Meta:
#     model = RegistryUserGroup
#     fields = ('url', 'group_name', 'owner_username',
#               'group', 'owner', 'description')
#     read_only_fields = ('group', )


##############################################################################
class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('name',)

##############################################################################


class PEImplementationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PEImplementation
        fields = (
            'id',
            'url',
            'description',
            'code',
            'parent_sig',
            'pckg',
            'name',
            'user',
            'workspace',
            'clone_of')
        read_only_fields = ('user', 'creation_date',)

##############################################################################


class FnImplementationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FnImplementation
        fields = (
            'id',
            'url',
            'description',
            'code',
            'parent_sig',
            'pckg',
            'name',
            'user',
            'workspace',
            'clone_of')
        read_only_fields = ('user', 'creation_date',)

##############################################################################


class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Workspace
        depth = 0
        fields = ('id', 'url', 'name', 'owner', 'description', 
                  'clone_of', 'creation_date')
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
        # TODO (nice-to-have) revisit the depth issue, user serialization is
        # not good enough - disabled for now.
        depth = 0
        read_only_fields = ('owner', 'creation_date')

    def transform_pes(self, obj, value):
        request = self.context.get('request')
        pes = obj.pesig_set.get_queryset()
        return map(lambda p: get_base_rest_uri(request) +
                   'pes/' +
                   str(p.id), pes)

    def transform_functions(self, obj, value):
        request = self.context.get('request')
        fns = obj.functionsig_set.get_queryset()
        return map(lambda p: get_base_rest_uri(request) +
                   'functions/' +
                   str(p.id), fns)

    def transform_literals(self, obj, value):
        request = self.context.get('request')
        lits = obj.literalsig_set.get_queryset()
        return map(lambda p: get_base_rest_uri(request) +
                   'literals/' +
                   str(p.id), lits)

    def transform_peimplementations(self, obj, value):
        request = self.context.get('request')
        peimpls = obj.peimplementation_set.get_queryset()
        return map(lambda p: get_base_rest_uri(request) +
                   'peimpls/' +
                   str(p.id), peimpls)

    def transform_fnimplementations(self, obj, value):
        request = self.context.get('request')
        fnimpls = obj.fnimplementation_set.get_queryset()
        return map(lambda p: get_base_rest_uri(request) +
                   'fnimpls/' +
                   str(p.id), fnimpls)


##############################################################################
class PESigSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PESig
        fields = (
            'url',
            'id',
            'workspace',
            'pckg',
            'name',
            'user',
            'description',
            'connections',
            'creation_date',
            'peimpls',
            'clone_of')
        read_only_fields = ('user', 'creation_date', )

##############################################################################


class ConnectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Connection
        # Pip package update 12/10/2018 (davve.ath) 
        # ADDED: fields, can't have empty fields
        fields = '__all__'


class FunctionParameterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FunctionParameter
        # Pip package update 12/10/2018 (davve.ath) 
        # ADDED: fields, can't have empty fields
        fields = '__all__'

##############################################################################


class FunctionSigSerializer(serializers.HyperlinkedModelSerializer):
    # implementations = serializers.WritableField
    #                   (source='fnimplementation_set', required=False)

    class Meta:
        model = FunctionSig
        fields = (
            'url',
            'id',
            'workspace',
            'pckg',
            'name',
            'user',
            'description',
            'creation_date',
            'return_type',
            'parameters',
            'fnimpls',
            'clone_of')
        read_only_fields = ('user', 'creation_date', )

##############################################################################


class LiteralSigSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = LiteralSig
        fields = (
            'url',
            'id',
            'workspace',
            'pckg',
            'name',
            'value',
            'description',
            'creation_date',
            'clone_of')
        read_only_fields = ('user', 'creation_date', )
