from django.contrib.auth.models import User, Group
from models import WorkspaceItem, Workspace, PESig, FunctionSig, LiteralSig, PEImplementation, FnImplementation
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', )

class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('id', 'name',)
    
class PEImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PEImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'group', 'workspace')
    
class FnImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FnImplementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'group', 'workspace')

class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
  #name = serializers.CharField(source='name')
  #owner = serializers.CharField(source='owner')
  #implementation_set = serializers.HyperlinkedRelatedField(many=True, view_name='implementation-detail')
  
  class Meta:
    model = Workspace
    # fields = ('id', 'name', 'owner', 'group',)
    depth = 0
    
class PESigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PESig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'group', 'description')

class FunctionSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = FunctionSig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'group', 'description')

class LiteralSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = LiteralSig
    fields = ('id', 'workspace', 'pckg', 'name', 'value',)
