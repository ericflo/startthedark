from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from events.views import events

urlpatterns = patterns('',
    url(
        r'^tonight/$', 
        events, 
        {'today': True, 'all_events': False, 'template_name': 'tonight.html'},
        name='ev_tonight'
    ),
    url(
        r'^archive/$', 
        events, 
        {'today': False, 'all_events': False, 'template_name': 'archive.html'},
        name='ev_archive'
    ),
    url(
        r'^everyone/tonight/$', 
        events, 
        {'today': True, 'all_events': True, 'template_name': 'tonight.html'},
        name='ev_everyone_tonight'
    ),
    url(
        r'^everyone/archive/$', 
        events, 
        {'today': False, 'all_events': True, 'template_name': 'archive.html'},
        name='ev_everyone_archive'
    ),
)