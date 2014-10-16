from django.contrib import admin
from vercereg.models import Workspace, PESig, LiteralSig, PEImplementation, FnImplementation, FunctionSig
import reversion


class PESigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')

class LiteralSigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  pass
    
class FunctionSigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')

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

class WorkspaceAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('name', 'owner', 'group', )  
  inlines = [PESigsInLine, FunctionSigsInLine]

admin.site.register(PESig, PESigAdmin)
admin.site.register(PEImplementation, PEImplementationAdmin)
admin.site.register(FnImplementation, FnImplementationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
