from django.conf.urls.defaults import *

urlpatterns = patterns('events.views',
    url(r'^tonight/$', 'tonight', name='ev_tonight'),
)