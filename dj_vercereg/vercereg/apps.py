from django.apps import AppConfig

# Pip package update 12/10/2018 (davve.ath) 
#  import watson

from watson import search as watson


class VerceRegConfig(AppConfig):
    name = 'vercereg'
    verbose_name = "VERCE dispel4py Registry"

    def ready(self):
        workspace = self.get_model('Workspace')
        pe = self.get_model('PESig')
        fun = self.get_model('FunctionSig')
        watson.register(workspace)
        watson.register(pe)
        watson.register(fun)
