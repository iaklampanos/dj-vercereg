from django.contrib import admin
from vercereg.models import Workspace, PESig, LiteralSig, PEImplementation, FnImplementation, FunctionSig, Connection
from guardian.admin import GuardedModelAdmin
from django.forms import TextInput, Textarea
from django.db import models
import reversion


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

class PESigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')
  inlines = [ConnectionInLine, PEImplInLine,]
  
  # def get_form(self, request, obj=None, **kwargs):
  #   # just save obj reference for future processing in Inline
  #   request._obj_ = obj
  #   return super(PESigAdmin, self).get_form(request, obj, **kwargs)
  
class LiteralSigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user', 'description', 'value')
    
class FunctionSigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')
  inlines = [FnImplInLine, ]

class PEImplementationAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('parent_sig', 'description', 'short_code')

class FnImplementationAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('parent_sig', 'description', 'short_code')
  
class PESigsInLine(admin.TabularInline):
  model = PESig
  extra = 1
  
  

class FunctionSigsInLine(admin.TabularInline):
  model = FunctionSig
  extra = 1

class WorkspaceAdmin(reversion.VersionAdmin, GuardedModelAdmin):
  list_display = ('name', 'description', 'owner', )  
  # inlines = [PESigsInLine, FunctionSigsInLine]

admin.site.register(PESig, PESigAdmin)
admin.site.register(FunctionSig, FunctionSigAdmin)
admin.site.register(LiteralSig, LiteralSigAdmin)
admin.site.register(PEImplementation, PEImplementationAdmin)
admin.site.register(FnImplementation, FnImplementationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
