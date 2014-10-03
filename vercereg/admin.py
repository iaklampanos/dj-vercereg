from django.contrib import admin
from vercereg.models import GenericDef, GenericSig, Workspace, PESig, LiteralSig, Implementation, FunctionSig

class PESigAdmin(admin.ModelAdmin):
  list_display = ('workspace', 'pckg', 'name', 'user', 'implementation_set')

class LiteralSigAdmin(admin.ModelAdmin):
  pass
  
class ImplementationAdmin(admin.ModelAdmin):
  pass
  
class FunctionSigAdmin(admin.ModelAdmin):
  pass

class ImplementationAdmin(admin.ModelAdmin):
  list_display = ('parent_sig', 'description', 'short_code')

class GenericSigsInLine(admin.TabularInline):
  model = GenericSig
  extra = 1

class PESigsInLine(admin.TabularInline):
  model = PESig
  extra = 1

class GenericDefsInLine(admin.TabularInline):
  model = GenericDef
  extra = 1

class WorkspaceAdmin(admin.ModelAdmin):
  list_display = ('name', 'owner', 'group', )
  inlines = [PESigsInLine, GenericSigsInLine, GenericDefsInLine]

class GenericDefAdmin(admin.ModelAdmin):
  # fields = ['workspace', 'pckg', 'name']
  list_display = ('workspace', 'pckg', 'name')

admin.site.register(GenericDef, GenericDefAdmin)
admin.site.register(PESig, PESigAdmin)
admin.site.register(Implementation, ImplementationAdmin)
admin.site.register(Workspace, WorkspaceAdmin)
