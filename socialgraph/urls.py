from django.conf.urls.defaults import *
from socialgraph.util import get_people_user_follows, get_people_following_user
from socialgraph.util import get_mutual_followers

urlpatterns = patterns('socialgraph.views',
    url(
        r'^followers/(?P<username>[a-zA-Z0-9_-]+)/$',
        'friend_list',
        {'friend_func': get_people_following_user},
        name='sg_followers'
    ),
    url(
        r'^following/(?P<username>[a-zA-Z0-9_-]+)/$',
        'friend_list',
        {'friend_func': get_people_user_follows},
        name='sg_following'
    ),
    url(
        r'^mutual/(?P<username>[a-zA-Z0-9_-]+)/$',
        'friend_list',
        {'friend_func': get_mutual_followers},
        name='sg_mutual'
    ),
    url(
        r'^follow/(?P<username>[a-zA-Z0-9_-]+)/$',
        'follow',
        name='sg_follow'
    ),
    url(
        r'^unfollow/(?P<username>[a-zA-Z0-9_-]+)/$',
        'unfollow',
        name='sg_unfollow'
    ),
)