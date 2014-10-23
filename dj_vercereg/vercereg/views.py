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
from vercereg.models import Workspace, PESig, FunctionSig, PEImplementation, FnImplementation, LiteralSig
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.filters import DjangoObjectPermissionsFilter
from vercereg.permissions import CustomObjectPermissions


class UserViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = User.objects.all()
  serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = Group.objects.all()
  serializer_class = GroupSerializer

class WorkspaceViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  
  queryset = Workspace.objects.all()
  serializer_class = WorkspaceSerializer
  filter_backends = (DjangoObjectPermissionsFilter,)
  permission_classes = (CustomObjectPermissions,)
  

  # list: list all workspaces the user has permissions to view
  # def list(self, request):
  #   queryset = Workspace.objects.all()
  #   serializer = WorkspaceSerializer(queryset, many=True, context={'request':request})
  #   return Response(serializer.data)

    # REMOVE LATER
    # if request.user.is_authenticated():
    #   queryset = Workspace.objects.all().filter(owner=request.user)
    # else:
    #   queryset = Workspace.objects.all()
    # serializer = WorkspaceSerializer(queryset, many=True, context={'request': request})
    # return Response(serializer.data)

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
