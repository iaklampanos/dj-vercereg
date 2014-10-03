from django.contrib.auth.models import User, Group
from models import WorkspaceItem, GenericDef, GenericSig, Workspace, PESig, LiteralSig, Implementation
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from rest_framework import serializers

class GenericDefSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = GenericDef
    fields = ('id', 'gendef_description', 'creation_date', 'user', 'group', 'workspace')

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', )

class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('id', 'name',)
    
class ImplementationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Implementation
    fields = ('description', 'code', 'parent_sig', 'pckg', 'name', 'user', 'group', 'workspace')

class WorkspaceSerializer(serializers.HyperlinkedModelSerializer):
  #name = serializers.CharField(source='name')
  #owner = serializers.CharField(source='owner')
  # genericdef_set = serializers.RelatedField(many=True)
  genericdef_set = serializers.HyperlinkedRelatedField(many=True, view_name='gendef-detail')
  implementation_set = serializers.HyperlinkedRelatedField(many=True, view_name='implementation-detail')
  
  class Meta:
    model = Workspace
    # fields = ('id', 'name', 'owner', 'group',)
    depth = 0
    
class PESigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = PESig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'group')

class LiteralSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = LiteralSig
    fields = ('id', 'workspace', 'pckg', 'name', 'value',)
    
class GenericSigSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = GenericSig
    fields = ('id', 'workspace', 'pckg', 'name', 'user', 'group')