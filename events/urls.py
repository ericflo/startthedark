from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from events import views

urlpatterns = patterns('',
    url(
        r'^tonight/$', 
        login_required(views.tonight), 
        {'everyone': False},
        name='ev_tonight'
    ),
    url(
        r'^archive/$', 
        login_required(views.archive), 
        {'everyone': False},
        name='ev_archive'
    ),
    url(
        r'^everyone/tonight/$', 
        views.tonight, 
        {'everyone': True},
        name='ev_everyone_tonight'
    ),
    url(
        r'^everyone/archive/$', 
        views.archive, 
        {'everyone': True},
        name='ev_everyone_archive'
    ),
    url(r'^event/(?P<id>\d+)/$', views.event, name="ev_event"),
    url(r'^create/$', views.create, name='ev_create'),
    url(
        r'^toggle-attendance/$', 
        views.toggle_attendance, 
        name='ev_toggle_attendance'
    ),
)