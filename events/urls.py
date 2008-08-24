from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from events import views

urlpatterns = patterns('',
    url(
        r'^tonight/$', 
        login_required(views.events), 
        {'today': True, 'all_events': False, 'template_name': 'tonight.html'},
        name='ev_tonight'
    ),
    url(
        r'^archive/$', 
        login_required(views.events), 
        {'today': False, 'all_events': False, 'template_name': 'archive.html'},
        name='ev_archive'
    ),
    url(
        r'^everyone/tonight/$', 
        views.events, 
        {'today': True, 'all_events': True, 'template_name': 'tonight.html'},
        name='ev_everyone_tonight'
    ),
    url(
        r'^everyone/archive/$', 
        views.events, 
        {'today': False, 'all_events': True, 'template_name': 'archive.html'},
        name='ev_everyone_archive'
    ),
    url(r'^create/$', views.create, name='ev_create'),
    url(
        r'^toggle-attendance/$', 
        views.toggle_attendance, 
        name='ev_toggle_attendance'
    ),
)