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

# Pip package update 12/10/2018 (davve.ath)
#  from django.conf.urls import patterns, include, url

from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from vercereg import views
from django.views.generic.base import RedirectView

# Pip package update 12/10/2018 (davve.ath)
from rest_framework.authtoken import views as tokenviews
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='VERCE dispel4py Registry')


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'groups', views.GroupViewSet, base_name='group')
router.register(r'registryusergroups', views.RegistryUserGroupViewSet, base_name='registryusergroup')
router.register(r'workspaces', views.WorkspaceViewSet, base_name='workspace')
router.register(r'pes', views.PESigViewSet, base_name='pesig')
router.register(r'functions', views.FunctionSigViewSet, base_name='functionsig')
router.register(r'literals', views.LiteralSigViewSet, base_name='literalsig')
router.register(r'connections', views.ConnectionViewSet, base_name='connection')
router.register(r'fnparams', views.FunctionParameterViewSet, base_name='functionparameter')
router.register(r'peimpls', views.PEImplementationViewSet)
router.register(r'fnimpls', views.FnImplementationViewSet)

# Pip package update 12/10/2018 (davve.ath)
#  urlpatterns = patterns('',

urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_vercereg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Pip package update 12/10/2018 (davve.ath)
    #  url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^docs/', schema_view),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    # url(r'^rest/$', 'api_root'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Pip package update 12/10/2018 (davve.ath)
    #  url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-token-auth/', tokenviews.obtain_auth_token)
]
#  )

# Admin-site specifics:
admin.site.site_header = 'VERCE Registry Admin'
admin.site.site_title = "VERCE Registry"
