from django.conf.urls.defaults import *

urlpatterns = patterns('socialgraph.views',
    url(
        r'^followers/(?P<username>[a-zA-Z0-9_-]+)/$',
        'friend_list',
        {'list_type': 'followers'},
        name='sg_followers'
    ),
    url(
        r'^following/(?P<username>[a-zA-Z0-9_-]+)/$',
        'friend_list',
        {'list_type': 'following'},
        name='sg_following'
    ),
    url(
        r'^mutual/(?P<username>[a-zA-Z0-9_-]+)/$',
        'friend_list',
        {'list_type': 'mutual'},
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
    url(
        r'^find-and-add/$',
        'find_and_add',
        name='sg_find_add'
    ),
)