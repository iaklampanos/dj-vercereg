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

from django.utils import timezone

from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from guardian.shortcuts import assign_perm

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import DjangoObjectPermissionsFilter
from rest_framework.response import Response
from rest_framework import status

from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import FunctionParameter
from vercereg.models import LiteralSig
from vercereg.models import PEImplementation
from vercereg.models import PESig
from vercereg.models import Workspace
from vercereg.models import RegistryUserGroup
from vercereg.models import Connection

from vercereg.permissions import UserAccessPermissions
from vercereg.permissions import WorkspaceBasedPermissions
from vercereg.permissions import WorkspaceItemPermissions
from vercereg.permissions import RegistryUserGroupAccessPermissions
from vercereg.permissions import ConnectionPermissions
from vercereg.permissions import FunctionParameterPermissions

from vercereg.serializers import FnImplementationSerializer
from vercereg.serializers import FunctionSigSerializer
from vercereg.serializers import GroupSerializer
from vercereg.serializers import RegistryUserGroupSerializer
# from vercereg.serializers import AdminRegistryUserGroupSerializer
from vercereg.serializers import LiteralSigSerializer
from vercereg.serializers import PEImplementationSerializer
from vercereg.serializers import PESigSerializer
from vercereg.serializers import UserSerializer
from vercereg.serializers import UserUpdateSerializer
from vercereg.serializers import WorkspaceSerializer
from vercereg.serializers import WorkspaceDeepSerializer
from vercereg.serializers import ConnectionSerializer
from vercereg.serializers import FunctionParameterSerializer

from rest_framework import permissions
from rest_framework.decorators import api_view

from django.db import transaction

from vercereg.utils import extract_id_from_url
from vercereg.utils import get_base_rest_uri
from vercereg.workspace_utils import WorkspaceCloner

import traceback
import sys

def set_workspace_default_permissions(wspc, user):
  '''Sets the default permissions to a newly created workspace.'''
  assign_perm('modify_contents_workspace', user, wspc)
  assign_perm('change_groupobjectpermission', user, wspc)
  assign_perm('add_userobjectpermission', user, wspc)
  assign_perm('vercereg.modify_contents_workspace', user, wspc)
  assign_perm('vercereg.view_contents_workspace', user, wspc)
  assign_perm('vercereg.view_meta_workspace', user, wspc)


class RegistryUserGroupViewSet(viewsets.ModelViewSet):
  ''' Registry user group resource.  '''

  permission_classes = (permissions.IsAuthenticated, RegistryUserGroupAccessPermissions)

  queryset = RegistryUserGroup.objects.all()
  serializer_class = RegistryUserGroupSerializer

  # def get_serializer_class(self):
  #   if self.request.user.is_superuser or self.request.user.is_staff:
  #     return AdminRegistryUserGroupSerializer
  #   else:
  #     return RegistryUserGroupSerializer

  @transaction.atomic
  def create(self, request):
    reqdata = request.DATA

    # Create a new group
    try:
      g = Group(name=reqdata['group_name'])
      g.save()
    except:
      return Response({'error when saving group':'name uniqueness constraint not satisfied or unknown internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Extract owner
    try:
      ownerurl = reqdata['owner']
      # FIXME Using manual id extraction, there must be a better way...
      oid = extract_id_from_url(ownerurl)
      o = User.objects.get(id=oid)
    except:
      return Response({'error resolving group owner':'the user may not exist in the DB, or bad request.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      rug = RegistryUserGroup(group=g, description=reqdata['description'], owner=o)
      rug.save()
    except:
      return Response({'error when saving registry user group':'internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = RegistryUserGroupSerializer(rug, many=False, context={'request':request})
    return Response(serializer.data)


  @transaction.atomic
  def update(self, request, pk=None):
    rug = RegistryUserGroup.objects.get(pk=pk)

    # Update the group:
    g = rug.group
    if (g.name != request.DATA['group_name']):
      g.name = request.DATA['group_name']
      g.save()

    # Update the registryusergroup
    # FIXME Using manual id extraction, there must be a better way...
    id = extract_id_from_url(request.DATA['owner'])
    user = User.objects.get(id=id)
    rug.owner = user
    rug.description = request.DATA['description']

    # Save the registryusergroup
    rug.save()
    serializer = RegistryUserGroupSerializer(rug, many=False, context={'request': request})
    return Response(serializer.data)



class WorkspaceViewSet(viewsets.ModelViewSet):
  ''' Workspace resource. '''
  permission_classes = (permissions.IsAuthenticated, WorkspaceBasedPermissions, )

  queryset = Workspace.objects.all()
  serializer_class = WorkspaceSerializer
  search_fields = ('^pckg', '^name', '@desciption', )

  def retrieve(self, request, pk=None):
    ''' Returns a workspace instance.
        ---
        parameters:
          - name: ls
            description: Lists the contents of the given workspace, as well as the packages contained.
            paramType: query
          - name: kind
            description: Lists details of the requested type of workspace item. Valid values are pes, functions, literals, peimpls and fnimpls.
            paramType: query
    '''
    allowed_kinds_to_show = ['pes', 'functions', 'literals', 'fn_implementations', 'pe_implementations']
    wspc = get_object_or_404(self.queryset, pk=pk)

    if 'ls' in self.request.QUERY_PARAMS:
      pes = list(PESig.objects.filter(workspace = wspc))
      functions = list(FunctionSig.objects.filter(workspace=wspc))
      literals = list(LiteralSig.objects.filter(workspace=wspc))
      fnimpls = list(FnImplementation.objects.filter(workspace=wspc))
      peimpls = list(PEImplementation.objects.filter(workspace=wspc))
      packages = []

      # collect all the packages
      pckg_set = set([])
      for i in pes+functions+literals+fnimpls+peimpls:
        pckg_set.add(i.pckg)
      packages = list(pckg_set)
      packages.sort()

      # FIXME: get_base_rest_uri depends on request - insecure - can be spoofed.
      dataret = {}
      dataret['pes'] = [{get_base_rest_uri(request)+'pes/' + str(x.id):x.pckg +'.' + x.name} for x in pes]
      dataret['functions'] = [{get_base_rest_uri(request)+'functions/' + str(x.id):x.pckg +'.' + x.name} for x in functions]
      dataret['literals'] = [{get_base_rest_uri(request)+'literals/' + str(x.id):x.pckg +'.' + x.name} for x in literals]
      dataret['peimpls'] = [{get_base_rest_uri(request)+'peimpls/' + str(x.id):x.pckg +'.' + x.name} for x in peimpls]
      dataret['fnimpls'] = [{get_base_rest_uri(request)+'fnimpls/' + str(x.id):x.pckg +'.' + x.name} for x in fnimpls]
      dataret['packages'] = packages

      return Response(dataret)

    kind_to_show = self.request.QUERY_PARAMS.get('kind')
    if not kind_to_show or kind_to_show not in allowed_kinds_to_show:
      self.check_object_permissions(request, wspc)
      serializer = WorkspaceDeepSerializer(wspc, context={'request': request})
      return Response(serializer.data)
    else:
      serializer = None
      items = []
      # FIXME: The repeated self.check_object_permissions(request, wspc) is probably not needed
      if kind_to_show == 'pes':
        items = PESig.objects.filter(workspace=wspc)
        self.check_object_permissions(request, wspc)
        serializer = PESigSerializer(items, many=True, context={'request': request})
      elif kind_to_show == 'functions':
        items = FunctionSig.objects.filter(workspace=wspc)
        self.check_object_permissions(request, wspc)
        serializer = FunctionSigSerializer(items, many=True, context={'request': request})
      elif kind_to_show == 'literals':
        items = LiteralSig.objects.filter(workspace=wspc)
        self.check_object_permissions(request, wspc)
        serializer = LiteralSigSerializer(items, many=True, context={'request': request})
      elif kind_to_show == 'fn_implementations':
        items = FnImplementation.objects.filter(workspace=wspc)
        self.check_object_permissions(request, wspc)
        serializer = FnImplementationSerializer(items, many=True, context={'request': request})
      elif kind_to_show == 'pe_implementations':
        items = PEImplementation.objects.filter(workspace=wspc)
        self.check_object_permissions(request, wspc)
        serializer = PEImplementationSerializer(items, many=True, context={'request': request})
      return Response(serializer.data)

  def create(self, request):
    '''
    Create a new workspace, or clone an existing one. In the case of cloning only the field name is taken into account.
    ---
    parameters:
      - name: name
        description: the name of the workspace.
      - name: description
        description: a textual description of the workspace.
      - name: clone_of
        description: indicates that a cloning operation is requested.
        paramType: query
        type: long
    '''
    clone_of = self.request.QUERY_PARAMS.get('clone_of')
    if not clone_of:
      return super(WorkspaceViewSet, self).create(request)

    # Check permissions
    try:
      cid = int(clone_of)
      or_wspc = Workspace.objects.get(id=cid)
      self.check_object_permissions(request, or_wspc)
    except ValueError:
      msg = {'error':'%s is not a valid workspace id'%(clone_of)}
      return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    except PermissionDenied:
      msg = {'error':'unauthorized access'}
      return Response(msg, status=status.HTTP_401_UNAUTHORIZED)
    except:
      msg = {'error':'could not retrieve workspace with id %s'%(clone_of)}
      return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    if not self.request.DATA.get('name'):
      msg = {'error':'name is required'}
      return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    cloner = WorkspaceCloner(or_wspc, self.request.DATA.get('name'), request.user)
    try:
      with transaction.atomic():
        cloned_workspace = cloner.clone()
    except:
      msg = {'error':'could not complete workspace cloning'}
      return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serializer = WorkspaceSerializer(cloned_workspace, many=False, context={'request': request})
    return Response(serializer.data)

  # def list(self, request):
  #   ''' Retrieve a list of workspaces.
  #       ---
  #       parameters:
  #         - name: search
  #           description: search terms for looking up workspaces
  #           type: string
  #   '''
  #   if self.request.QUERY_PARAMS.get('search'):
  #       # resort to default bahaviour
  #       return super(WorkspaceViewSet, self).list(request)
  #   allowed_workspaces = []
  #   for w in self.queryset:
  #     try:
  #       self.check_object_permissions(request, w)
  #       allowed_workspaces.append(w)
  #     except:
  #       pass
  #   serializer = WorkspaceSerializer(allowed_workspaces, many=True, context={'request': request})
  #   return Response(serializer.data)

  def pre_save(self, obj):
    obj.creation_date = timezone.now()
    if not obj.pk: # this is an update
      obj.owner = self.request.user

  def post_save(self, obj, created):
    if created:
      assign_perm('vercereg.modify_meta_workspace', self.request.user, obj)
      assign_perm('vercereg.modify_contents_workspace', self.request.user, obj)
      assign_perm('vercereg.view_contents_workspace', self.request.user, obj)
      assign_perm('vercereg.view_meta_workspace', self.request.user, obj)
      # TODO: Add change/delete workspace - don't know what's the correct permissions to set / Internet


class UserViewSet(viewsets.ModelViewSet):
  ''' User resource. '''
  permission_classes = (permissions.IsAuthenticated, UserAccessPermissions)

  queryset = User.objects.all()
  serializer_class = UserSerializer

  def list(self, request):
    ''' Returns a list of users. '''
    allowed_users = []
    for u in self.queryset:
      try:
        self.check_object_permissions(request, u)
        allowed_users.append(u)
      except:
        pass
    serializer = UserSerializer(allowed_users, many=True, context={'request': request})
    # serializer = UserSerializer(allowed_users, many=True)
    return Response(serializer.data)

  def create(self, request):
    ''' Creates a new user in the registry. '''
    # Performs the following: It creates a new user, it creates a new registry user group (with its associated group), it assigns the new user as the owner of the group, and it finally makes user a member of the new group. It returns the regular serialized version of the newly created user. (https://github.com/iaklampanos/dj-vercereg/wiki/Creating-users)
    reqdata = request.DATA

    try:
      u = User.objects.create_user(username=reqdata['username'], password=reqdata['password'], email=reqdata['email'], first_name=reqdata['first_name'], last_name=reqdata['last_name'])
      u.first_name = reqdata['first_name']
      u.last_name = reqdata['last_name']
      u.save()
    except:
      msg={'error when creating user':'username already exists or unknown error'}
      return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # create a group for this user, which the user will own
    try:
      # g = Group(name=reqdata['username'])
      g = Group.objects.create(name=reqdata['username'])
      g.user_set.add(u)
      g.save()
    except:
      if u.pk: u.delete()
      return Response({'error when saving group':'name uniqueness constraint not satisfied or unknown internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # attempts to add the new user to the global read-all user group
    try:
      read_all_group = Group.objects.get(name='default_read_all_group')
      read_all_group.user_set.add(u)
      read_all_group.save()
    except:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      traceback.print_tb(exc_traceback)

    try:
      desc = 'Default group for user ' + u.username + '.'
      rug = RegistryUserGroup(group=g, description=desc, owner=u)
      rug.save()
    except:
      if g.pk: g.delete()
      if u.pk: u.delete()
      return Response({'error when saving registry user group':'internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    serializer = UserSerializer(u, context={'request': request})
    return Response(serializer.data)

  def get_serializer_class(self):
    if self.request.method in permissions.SAFE_METHODS or self.request.method=='POST':
      return UserSerializer
    # elif self.request.method=='PUT':
    else:
      return UserUpdateSerializer




class GroupViewSet(viewsets.ModelViewSet):
  ''' Basic user group resource. '''

  permission_classes = (permissions.IsAuthenticated, )

  queryset = Group.objects.all()
  serializer_class = GroupSerializer



class LiteralSigViewSet(viewsets.ModelViewSet):
  ''' Literal entities resource. '''
  permission_classes = (permissions.IsAuthenticated, WorkspaceItemPermissions, )

  queryset = LiteralSig.objects.all()
  serializer_class = LiteralSigSerializer

  def pre_save(self, obj):
    obj.creation_date = timezone.now()
    if not obj.pk:
      obj.user = self.request.user


class PESigViewSet(viewsets.ModelViewSet):
  ''' PE resource. Allows addition and manipulation of dispel4py processing elements (PEs). '''
  permission_classes = (permissions.IsAuthenticated, WorkspaceItemPermissions, )

  queryset = PESig.objects.all()
  serializer_class = PESigSerializer

  # def list(self, request):
  #   viewable = []
  #   for pe in self.queryset:
  #     try:
  #       self.check_object_permissions(request, pe)
  #       viewable.append(pe)
  #     except:
  #       pass
  #   serializer = PESigSerializer(viewable, many=True, context={'request':request})
  #   return Response(serializer.data)

  def pre_save(self, obj):
    obj.creation_date = timezone.now()
    if not obj.pk:
      obj.user = self.request.user


class FunctionSigViewSet(viewsets.ModelViewSet):
  ''' Function resource. Allows addition and manipulation of dispel4py functions. '''
  permission_classes = (permissions.IsAuthenticated, WorkspaceItemPermissions,)

  queryset = FunctionSig.objects.all()
  serializer_class = FunctionSigSerializer

  def pre_save(self, obj):
    obj.creation_date = timezone.now()
    if not obj.pk:
      obj.user = self.request.user


class FunctionParameterViewSet(viewsets.ModelViewSet):
  ''' Function parameter resource. Allows the addition and manipulation of function parameters. Function parameters are associated with functions and are not themselves workspace items. '''
  permission_classes = (permissions.IsAuthenticated, FunctionParameterPermissions, )
  queryset = FunctionParameter.objects.all()
  serializer_class = FunctionParameterSerializer

  def list(self, request):
    message = {'error':'listing function parameters is not permitted'}
    return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ConnectionViewSet(viewsets.ModelViewSet):
  ''' PE Connection resource. Allows the addition and manipulation of PE connections. Connections are associated with PEs and are not themselves workspace items. '''
  permission_classes = (permissions.IsAuthenticated, ConnectionPermissions)
  queryset = Connection.objects.all()
  serializer_class = ConnectionSerializer

  # Disable list view
  def list(self, request):
    message = {'error':'listing connections is not permitted'}
    #TODO: Use a more appropriate ERROR code
    return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PEImplementationViewSet(viewsets.ModelViewSet):
  ''' PE Implementation resource. Allows the creation and manipulation of PE implementations. PEs may have one or more implementations. '''
  permission_classes = (permissions.IsAuthenticated, WorkspaceItemPermissions,)

  queryset = PEImplementation.objects.all()
  serializer_class = PEImplementationSerializer

  def pre_save(self, obj):
    obj.creation_date = timezone.now()
    if not obj.pk:
      obj.user = self.request.user



class FnImplementationViewSet(viewsets.ModelViewSet):
  ''' Function implementation resource. Allows the creation and manipulation of function implementations. Function entities may have one or more implementations. '''
  permission_classes = (permissions.IsAuthenticated, WorkspaceItemPermissions,)

  queryset = FnImplementation.objects.all()
  serializer_class = FnImplementationSerializer

  def pre_save(self, obj):
    obj.creation_date = timezone.now()
    if not obj.pk:
      obj.user = self.request.user
