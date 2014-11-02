from datetime import datetime

from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from guardian.shortcuts import assign_perm

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import DjangoObjectPermissionsFilter
from rest_framework.response import Response

from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import LiteralSig
from vercereg.models import PEImplementation
from vercereg.models import PESig
from vercereg.models import Workspace
from vercereg.models import RegistryUserGroup

from vercereg.permissions import UserAccessPermissions
from vercereg.permissions import WorkspaceBasedPermissions
from vercereg.permissions import WorkspaceItemPermissions
from vercereg.permissions import RegistryUserGroupAccessPermissions

from vercereg.serializers import FnImplementationSerializer
from vercereg.serializers import FunctionSigSerializer
from vercereg.serializers import GroupSerializer
from vercereg.serializers import RegistryUserGroupSerializer
from vercereg.serializers import LiteralSigSerializer
from vercereg.serializers import PEImplementationSerializer
from vercereg.serializers import PESigSerializer
from vercereg.serializers import UserSerializer
from vercereg.serializers import UserUpdateSerializer
from vercereg.serializers import WorkspaceSerializer
from vercereg.serializers import WorkspaceDeepSerializer

from rest_framework import permissions 
from rest_framework.decorators import api_view


def set_workspace_default_permissions(wspc, user):
  ''' Sets the default permissions to a newly created workspace, whose creator is user '''
  assign_perm('modify_contents_workspace', user, wspc)
  assign_perm('change_groupobjectpermission', user, wspc)
  assign_perm('add_userobjectpermission', user, wspc)
  assign_perm('vercereg.modify_contents_workspace', user, wspc)
  assign_perm('vercereg.view_contents_workspace', user, wspc)
  assign_perm('vercereg.view_meta_workspace', user, wspc)
  

class WorkspaceViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, WorkspaceBasedPermissions, )
  
  queryset = Workspace.objects.all()
  serializer_class = WorkspaceSerializer
  
  def retrieve(self, request, pk=None):
    wspc = get_object_or_404(self.queryset, pk=pk)
    self.check_object_permissions(request, wspc)
    serializer = WorkspaceDeepSerializer(wspc, context={'request': request})
    return Response(serializer.data)
  
  def list(self, request):
    allowed_workspaces = []
    for w in self.queryset:
      try:
        self.check_object_permissions(request, w)
        allowed_workspaces.append(w)
      except:
        pass
    serializer = WorkspaceSerializer(allowed_workspaces, many=True, context={'request': request})
    return Response(serializer.data)
  
  def pre_save(self, obj):
    obj.creation_date = datetime.now()
    if not obj.pk:
      obj.owner = self.request.user


class UserViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, UserAccessPermissions)
  
  queryset = User.objects.all()
  serializer_class = UserSerializer
  
  def list(self, request):
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

  def get_serializer_class(self):
    if self.request.method in permissions.SAFE_METHODS or self.request.method=='POST':
      return UserSerializer
    # elif self.request.method=='PUT':
    else:
      return UserUpdateSerializer

  

# class RegistryUserGroupViewSet(viewsets.ModelViewSet):
#   permission_classes = (permission_classes.IsAuthenticated, )
#
#   queryset = RegistryUserGroup.objects.all()
#   serializer_class = GroupSerializer
  
    
class RegistryUserGroupViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = RegistryUserGroup.objects.all()
  serializer_class = RegistryUserGroupSerializer
  
  def create(self, request):
    return Response('')
  
class GroupViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, )

  queryset = Group.objects.all()
  serializer_class = GroupSerializer


class LiteralSigViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = LiteralSig.objects.all()
  serializer_class = LiteralSigSerializer


class PESigViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = PESig.objects.all()
  serializer_class = PESigSerializer


class FunctionSigViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = FunctionSig.objects.all()
  serializer_class = FunctionSigSerializer


class PEImplementationViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = PEImplementation.objects.all()
  serializer_class = PEImplementationSerializer


class FnImplementationViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = FnImplementation.objects.all()
  serializer_class = FnImplementationSerializer
