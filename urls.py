from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from events.views import events
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name="index"),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/about.html'}, name="about"),
    url(r'^open-source/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/open_source.html'}, name="opensource"),
    (r'^events/', include('events.urls')),
    (r'^friends/', include('socialgraph.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^profile/', include('profile.urls')),
    url(
        r'^settings/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/settings.html'}, 
        name='settings'
    ),
    (r'^admin/(.*)', admin.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
