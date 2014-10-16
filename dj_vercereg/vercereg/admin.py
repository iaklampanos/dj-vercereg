from django.contrib import admin
from vercereg.models import GenericDef, GenericSig, Workspace, PESig, LiteralSig, Implementation, FunctionSig
import reversion


class PESigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user', 'implementation_set')

class LiteralSigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  pass
    
class FunctionSigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  pass

class ImplementationAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('parent_sig', 'description', 'short_code')

class GenericSigsInLine(reversion.VersionAdmin, admin.TabularInline):
  model = GenericSig
  extra = 1

class PESigsInLine(reversion.VersionAdmin, admin.TabularInline):
  model = PESig
  extra = 1

class GenericDefsInLine(reversion.VersionAdmin, admin.TabularInline):
  model = GenericDef
  extra = 1

class WorkspaceAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('name', 'owner', 'group', )
  inlines = [PESigsInLine, GenericSigsInLine, GenericDefsInLine]

class GenericDefAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  # fields = ['workspace', 'pckg', 'name']
  list_display = ('workspace', 'pckg', 'name')

admin.site.register(GenericDef, GenericDefAdmin)
admin.site.register(PESig, PESigAdmin)
admin.site.register(Implementation, ImplementationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
