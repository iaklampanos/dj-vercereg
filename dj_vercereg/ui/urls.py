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
