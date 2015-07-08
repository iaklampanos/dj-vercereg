from django.contrib import admin
from django.db import models

from django.contrib.auth.models import User
from vercereg.models import Workspace

class FavouriteWorkspaces(models.Model):
    user = models.ForeignKey(User)
    workspace = models.ForeignKey(Workspace)
    
    def __unicode__(self):
        return u'%s faved %s - %s' % (self.user.username,
                                      self.workspace.name,
                                      self.workspace.owner.username)
    
    class Meta:
        unique_together = ('user', 'workspace', )

admin.site.register(FavouriteWorkspaces)
