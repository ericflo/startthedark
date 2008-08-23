from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from socialgraph.models import UserLink

def friend_list(request, username, subset_func=None):
    user = get_object_or_404(User, username=username)
    if subset_func is None:
        raise Http404
    context = {
        'friends': subset_func(user),
    }
    return render_to_response(
        'socialgraph/friend_list.html',
        context,
        context_instance = RequestContext(request)
    )

def follow(request, username):
    user = get_object_or_404(User, username=username)
    ul, created = UserLink.objects.get_or_create(from_user=request.user, 
        to_user=user)
    context = {
        'other_user': user,
        'created': created,
    }
    return render_to_response(
        'socialgraph/followed.html',
        context,
        context_instance = RequestContext(request)
    )
follow = login_required(follow)

def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    try:
        ul = UserLink.objects.get(from_user=request.user, to_user=user)
        ul.delete()
        deleted = True
    except UserLink.DoesNotExist:
        deleted = False
    context = {
        'other_user': user,
        'deleted': deleted,
    }
    return render_to_response(
        'socialgraph/unfollowed.html',
        context,
        context_instance = RequestContext(request)
    )
unfollow = login_required(unfollow)