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

from django.contrib import admin
from vercereg.models import Workspace
from vercereg.models import PESig
from vercereg.models import LiteralSig
from vercereg.models import PEImplementation
from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import Connection
from vercereg.models import RegistryUserGroup
from guardian.admin import GuardedModelAdmin
from django.forms import TextInput, Textarea
from django.db import models
import reversion
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import watson

# Pip package update 12/10/2018 (davve.ath) 
# Refactored package names
from reversion.admin import VersionAdmin
from watson.admin import SearchAdmin

class PEImplInLine(admin.StackedInline):
    model = PEImplementation
    extra = 1

    # def get_form(self, request, obj=None, **kwargs):
    #   self.exclude = []
    #   self.exclude.append('workspace')
    #   return super(PEImplInLine, self).get_form(request, obj, **kwargs)

    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #   field = super(PEImplInLine, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #
    #   if db_field.name == 'workspace':
    #     print ' >1> ' + str(db_field.name)
    #     print ' *2* ' + str(request._obj_.workspace)
    #     print ' $3$ ' + str(field)
    #     if request._obj_ is not None:
    #       field.queryset = field.queryset.none()
    #       field.queryset = field.queryset.filter(workspace__exact = request._obj_.workspace)
    #     else:
    #       field.queryset = field.queryset.none()
    #   return field

class FnImplInLine(admin.StackedInline):
    model = FnImplementation
    extra = 1

class ConnectionInLine(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':30})},
    }
    model = Connection
    extra = 1

# Pip package update 12/10/2018 (davve.ath) 
#  class PESigAdmin(reversion.VersionAdmin, GuardedModelAdmin, watson.SearchAdmin):

class PESigAdmin(VersionAdmin, GuardedModelAdmin, SearchAdmin):
                 # admin.ModelAdmin):
    list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')
    inlines = [ConnectionInLine, PEImplInLine,]
    search_fields = ('description', 'name',)

    # def get_form(self, request, obj=None, **kwargs):
    #   # just save obj reference for future processing in Inline
    #   request._obj_ = obj
    #   return super(PESigAdmin, self).get_form(request, obj, **kwargs)

# Pip package update 12/10/2018 (davve.ath) 
#  class LiteralSigAdmin(reversion.VersionAdmin, GuardedModelAdmin, watson.SearchAdmin):

class LiteralSigAdmin(VersionAdmin, GuardedModelAdmin, SearchAdmin):
    list_display = ('workspace', 'pckg', 'name', 'user', 'description', 'value')
    search_fields = ('name', 'description', 'value')

# Pip package update 12/10/2018 (davve.ath) 
#  class FunctionSigAdmin(reversion.VersionAdmin, GuardedModelAdmin, watson.SearchAdmin):

class FunctionSigAdmin(VersionAdmin, GuardedModelAdmin, SearchAdmin):
                       # admin.ModelAdmin):
    list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')
    inlines = [FnImplInLine, ]
    search_fields = ('description', 'name',)


# Pip package update 12/10/2018 (davve.ath) 
#  class PEImplementationAdmin(reversion.VersionAdmin, admin.ModelAdmin):

class PEImplementationAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('parent_sig', 'description', 'short_code')

# Pip package update 12/10/2018 (davve.ath) 
#  class FnImplementationAdmin(reversion.VersionAdmin, admin.ModelAdmin):

class FnImplementationAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('parent_sig', 'description', 'short_code')

class PESigsInLine(admin.TabularInline):
    model = PESig
    extra = 1

class FunctionSigsInLine(admin.TabularInline):
    model = FunctionSig
    extra = 1

# Pip package update 12/10/2018 (davve.ath) 
#  class WorkspaceAdmin(reversion.VersionAdmin,
                     #  GuardedModelAdmin,
                     #  watson.SearchAdmin):

class WorkspaceAdmin(VersionAdmin,
                     GuardedModelAdmin,
                     SearchAdmin):
    list_display = ('name', 'description', 'owner', )
    search_fields = ('name', 'description',)
    # inlines = [PESigsInLine, FunctionSigsInLine]


class RegistryUserGroupInline(admin.StackedInline):
    model = RegistryUserGroup
    can_delete = False

class GroupAdmin(GroupAdmin):
    inlines = [RegistryUserGroupInline]



admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(PESig, PESigAdmin)
admin.site.register(FunctionSig, FunctionSigAdmin)
admin.site.register(LiteralSig, LiteralSigAdmin)
admin.site.register(PEImplementation, PEImplementationAdmin)
admin.site.register(FnImplementation, FnImplementationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
