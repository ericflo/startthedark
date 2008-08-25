from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from events.views import events
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    url(
        r'^$', 
        login_required(events), 
        {'today': True, 'all_events': False, 'template_name': 'tonight.html'},
        name='index'
    ),
    (r'^events/', include('events.urls')),
    (r'^friends/', include('socialgraph.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_URL, 'show_indexes': True}),
)
