from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from socialgraph.util import get_people_user_follows, get_people_following_user
from socialgraph.util import get_mutual_followers
from events.models import Event, Attendance

def detail(request, username=None):
    """
    Renders information about a single user's profile.  This includes
    information about who follows them, who they follow, mutual followers, the
    latest events created, and whether the currently logged in user is a friend
    of the user to render.
    """
    user = get_object_or_404(User, username=username)
    events_created = list(Event.objects.filter(creator=user, latest=True).order_by('-creation_date')[:10])
    attended = Attendance.objects.filter(user=user).order_by('-registration_date')[:10]
    events_attended = list(Event.objects.filter(id__in=[e.event.id for e in attended]).order_by('-creation_date'))
    people_following_user = get_people_following_user(user)
    context = {
        'profile_user': user,
        'people_following_user': people_following_user,
        'people_user_follows': get_people_user_follows(user),
        'mutual_followers': get_mutual_followers(user),
        'events_created': events_created,
        'num_events_created': len(events_created),
        'events_attended': events_attended,
        'num_events_attended': len(events_attended),
        'friend': request.user in people_following_user,
    }
    return render_to_response(
        'profile/detail.html',
        context,
        context_instance = RequestContext(request)
    )
    