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


from django.conf.urls import patterns, url

from ui import views
from dj_vercereg.settings import LOGIN_URL


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/ui/'}, name='logout'),
    url(r'^workspace/(?P<workspace_id>\d+)/$',
        'ui.views.view_workspace', name='workspace_detail'),
    url(r'^$', 'ui.views.index', name='index'),
    
    # favourites JSON response, meant for AJAX
    url(r'^ajax/toggle_faved/(?P<workspace_id>\d+)/$',
        'ui.views.toggle_workspace_fav',
        name='toggle_workspace_fav'),
    
    url(r'^ajax/faved/(?P<workspace_id>\d+)/$',
        'ui.views.is_workspace_faved',
        name='is_workspace_faved'),
    
    url(r'^flow/(?P<workspace_id>\d+)/$', 
        'ui.views.flow', name='flow'),
)
