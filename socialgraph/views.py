from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from socialgraph.models import UserLink
from socialgraph.util import get_people_user_follows, get_people_following_user
from socialgraph.util import get_mutual_followers
from socialgraph.forms import SearchForm

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

FRIEND_FUNCTION_MAP = {
    'followers': get_people_user_follows,
    'following': get_people_following_user,
    'mutual': get_mutual_followers,
}

def friend_list(request, list_type, username):
    """
    Renders a list of friends, as returned by the function retrieved from the
    ``FRIEND_FUNCTION_MAP``, given the user specified by the username in the
    URL.
    """
    user = get_object_or_404(User, username=username)
    context = {
        'list_type': list_type,
        'friends': FRIEND_FUNCTION_MAP[list_type](user),
    }
    return render_to_response(
        'socialgraph/friend_list.html',
        context,
        context_instance = RequestContext(request)
    )

def follow(request, username):
    """
    Adds a "following" edge from the authenticated user to the user specified by
    the username in the URL.
    """
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
    """
    Removes a "following" edge from the authenticated user to the user specified
    by the username in the URL.
    """
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

def find_and_add(request):
    """
    A page for finding and adding new friends to follow.  Right now this
    consists solely of a search box, which given input, renders a list of
    users who match the search terms.
    """
    search_form = SearchForm(request.GET or None)
    context = {
        'search_form': search_form,
    }
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        context['q'] = q
        users = User.objects.filter(username__icontains=q) | User.objects.filter(
            email__icontains=q)
    else:
        users = []
    friends = get_people_user_follows(request.user)
    users = [(u, u in friends) for u in users]
    context['users'] = users
    context['user_count'] = len(users)
    return render_to_response(
        'socialgraph/find_add.html',
        context,
        context_instance = RequestContext(request)
    )
find_and_add = login_required(find_and_add)