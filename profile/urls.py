from django.conf.urls.defaults import *

urlpatterns = patterns('profile.views',
    url(r'^detail/(?P<username>[a-zA-Z0-9_-]+)/$', 'detail', 
        name='profile_detail'),
)