from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from socialgraph.models import UserLink

def _get_next(request):
    """
    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    return request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

def friend_list(request, username, friend_func=None):
    user = get_object_or_404(User, username=username)
    if friend_func is None:
        raise Http404
    return render_to_response(
        'socialgraph/friend_list.html',
        {'friends': friend_func(user)},
        context_instance = RequestContext(request)
    )

def follow(request, username):
    user = get_object_or_404(User, username=username)
    ul, created = UserLink.objects.get_or_create(from_user=request.user, 
        to_user=user)
    next = _get_next(request)
    if next and next != request.path:
        request.user.message_set.create(
            message=_('You are now following %s') % user.username)
        return HttpResponseRedirect(next)
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
    next = _get_next(request)
    if next and next != request.path:
        request.user.message_set.create(
            message=_('You are no longer following %s') % user.username)
        return HttpResponseRedirect(next)
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