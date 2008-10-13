from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name="index"),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/about.html'}, name="about"),
    url(r'^open-source/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/open_source.html'}, name="opensource"),
    url(r'^help/$', 'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/help.html'}, name="help"),
    (r'^events/', include('events.urls')),
    (r'^friends/', include('socialgraph.urls')),
    (r'^accounts/', include('registration.urls')),
    url(r'^accounts/latest/$',
        login_required(object_list),
        {'queryset': User.objects.order_by('-date_joined'),
        'paginate_by': 50, 'allow_empty': True},
        name='user_list'),
    (r'^profile/', include('profile.urls')),
    url(
        r'^settings/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template': 'misc/settings.html'}, 
        name='settings'
    ),
    (r'^admin/(.*)', admin.site.root),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
