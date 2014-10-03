from django.shortcuts import render
from rest_framework import viewsets
from vercereg.serializers import GenericDefSerializer
from vercereg.serializers import GenericSigSerializer
from vercereg.serializers import UserSerializer
from vercereg.serializers import GroupSerializer
from vercereg.serializers import WorkspaceSerializer
from vercereg.serializers import PESigSerializer
from vercereg.serializers import LiteralSigSerializer
from vercereg.serializers import ImplementationSerializer
from vercereg.models import GenericDef, Workspace, PESig, Implementation, LiteralSig, GenericSig
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import permissions


class GenericDefViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = GenericDef.objects.all()
  serializer_class = GenericDefSerializer

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
  base_name = 'workspace'
  serializer_class = WorkspaceSerializer

  def list(self, request):
    if request.user.is_authenticated():
      queryset = Workspace.objects.all().filter(owner=request.user)
    else:
      queryset = Workspace.objects.all()
    serializer = WorkspaceSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

class LiteralSigViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = LiteralSig.objects.all()
  serializer_class = LiteralSigSerializer

class GenericSigViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = GenericSig.objects.all()
  serializer_class = GenericSigSerializer
  
class PESigViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = PESig.objects.all()
  serializer_class = PESigSerializer
  
class ImplementationViewSet(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)

  queryset = Implementation.objects.all()
  serializer_class = ImplementationSerializer
  
