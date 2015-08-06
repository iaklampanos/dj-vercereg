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
