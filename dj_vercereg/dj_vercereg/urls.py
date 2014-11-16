from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from vercereg import views
from django.views.generic.base import RedirectView


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
router.register(r'peimpls', views.PEImplementationViewSet, base_name='pe_implementation')
router.register(r'fnimpls', views.FnImplementationViewSet, base_name='fn_implementation')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_vercereg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    # url(r'^rest/$', 'api_root'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^docs/', include('rest_framework_swagger.urls')),

)

# Admin-site specifics:
admin.site.site_header = 'VERCE Registry Admin'
admin.site.site_title = "VERCE Registry"