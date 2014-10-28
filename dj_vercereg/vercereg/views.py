from django.shortcuts import render
from rest_framework import viewsets
from vercereg.serializers import UserSerializer
from vercereg.serializers import GroupSerializer
from vercereg.serializers import WorkspaceSerializer
from vercereg.serializers import PESigSerializer
from vercereg.serializers import LiteralSigSerializer
from vercereg.serializers import PEImplementationSerializer
from vercereg.serializers import FnImplementationSerializer
from vercereg.serializers import FunctionSigSerializer
from vercereg.serializers import WorkspaceDeepSerializer
from vercereg.models import Workspace, PESig, FunctionSig, PEImplementation, FnImplementation, LiteralSig
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.filters import DjangoObjectPermissionsFilter
from vercereg.permissions import WorkspaceBasedPermissions
from vercereg.permissions import WorkspaceItemPermissions
from django.shortcuts import get_object_or_404


from guardian.shortcuts import assign_perm


def set_workspace_default_permissions(wspc, user):
  ''' Sets the default permissions to a newly created workspace, whose creator is user '''
  assign_perm('modify_contents_workspace', user, wspc)
  assign_perm('change_groupobjectpermission', user, wspc)
  assign_perm('add_userobjectpermission', user, wspc)
  assign_perm('vercereg.modify_contents_workspace', user, wspc)
  assign_perm('vercereg.view_contents_workspace', user, wspc)
  assign_perm('vercereg.view_meta_workspace', user, wspc)
  
  
class WorkspaceViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, WorkspaceBasedPermissions,  )
  
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
    obj.owner = self.request.user
    
  # def create(self, request):
  #   serializer = WorkspaceSerializer(many=False, context={'request':request})
  #   return Response(serializer.data)
  
  def update(self, request):
    pass

class UserViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = User.objects.all()
  serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

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
