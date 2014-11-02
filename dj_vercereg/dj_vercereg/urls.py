from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from vercereg import views

router = routers.DefaultRouter()
router.register(r'rest/users', views.UserViewSet, base_name='user')
router.register(r'rest/groups', views.GroupViewSet, base_name='group')
router.register(r'rest/registryusergroups', views.RegistryUserGroupViewSet, base_name='registryusergroup')
router.register(r'rest/workspaces', views.WorkspaceViewSet, base_name='workspace')
router.register(r'rest/pes', views.PESigViewSet, base_name='pesig')
router.register(r'rest/literals', views.LiteralSigViewSet, base_name='literalsig')
router.register(r'rest/pe_implementations', views.PEImplementationViewSet, base_name='pe_implementation')
router.register(r'rest/fn_implementations', views.FnImplementationViewSet, base_name='fn_implementation')


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_vercereg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)

# Admin-site specifics:
admin.site.site_header = 'VERCE Registry Admin'
admin.site.site_title = "VERCE Registry"