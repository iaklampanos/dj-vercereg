from django.contrib import admin
from vercereg.models import Workspace, PESig, LiteralSig, PEImplementation, FnImplementation, FunctionSig, Connection
import reversion


class PEImplInLine(admin.StackedInline):
  model = PEImplementation
  extra = 1
  
class FnImplInLine(admin.StackedInline):
  model = FnImplementation
  extra = 1

class ConnectionInLine(admin.TabularInline):
  model = Connection
  extra = 1

class PESigAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user') #, 'implementation_set')
  inlines = [ConnectionInLine, PEImplInLine,]
  
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

class WorkspaceAdmin(reversion.VersionAdmin, admin.ModelAdmin):
  list_display = ('name', 'description', 'owner', 'group', )  
  inlines = [PESigsInLine, FunctionSigsInLine]

admin.site.register(PESig, PESigAdmin)
admin.site.register(FunctionSig, FunctionSigAdmin)
admin.site.register(LiteralSig, LiteralSigAdmin)
admin.site.register(PEImplementation, PEImplementationAdmin)
admin.site.register(FnImplementation, FnImplementationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
