from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from events.models import Event, Attendance
from events.forms import EventForm
from dateutil.parser import parse
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse

def tonight(request, everyone=True):
    """
    Renders a list of ``Event`` instances, which are selected mainly based on
    two factors:
    
    The ``everyone`` parameter:
        If this is set to False, then we filter down the event list to be only
        those events that were created by or attended by one of the people who
        the user follows.
    
    The user's authentication:
        If the user is authenticated, the user's events are separated from the
        other events.
    """
    events = Event.objects.today().filter(latest=True)
    if request.user.is_authenticated():
        my_events = events.filter(creator=request.user) | events.filter(
            attendance__user=request.user)
        events = events.exclude(creator=request.user).exclude(
            attendance__user=request.user)
        following = request.user.following_set.all().values_list('to_user', 
            flat=True)
    else:
        my_events = Event.objects.none()
        following = None
    if not everyone:
        events = events.filter(creator__in=following) | events.filter(
            attendance__user__in=following)
    events = events.order_by('-start_date', '-creation_date').distinct()
    context = {
        'events': events,
        'my_events': my_events,
        'following': following,
        'event_form': EventForm(),
    }
    return render_to_response(
        'events/tonight.html',
        context,
        context_instance = RequestContext(request)
    )

def archive(request, everyone=True):
    """
    Renders a list of ``Event`` instances, which are selected mainly based on
    one parameter:
    
    ``everyone``:
        If this is set to False, then we filter down the event list to be only
        those events that were created by or attended by one of the people who
        the user follows.
    """
    events = Event.objects.filter(latest=True) | Event.objects.filter(
        attendance__user__isnull=False)
    if request.user.is_authenticated():
        following = list(request.user.following_set.all().values_list('to_user', 
            flat=True))
    else:
        following = None
    if not everyone:
        following.append(request.user.id)
        events = events.filter(creator__in=following) | events.filter(
            attendance__user__in=following)
    events = events.order_by('-creation_date', '-start_date').distinct()
    context = {
        'events': events,
        'following': following,
    }
    return render_to_response(
        'events/archive.html',
        context,
        context_instance = RequestContext(request)
    )

def event(request, id):
    """
    Render a single event.
    """
    event = get_object_or_404(Event, id=id)
    return render_to_response(
        'events/event_details.html',
        {'event': event},
        context_instance = RequestContext(request)
    )

def create(request):
    """
    Renders a form for creating a new ``Event`` instance, validates against that
    form, and creates the new instances.
    """
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.creator = request.user
        guessed_date = None
        # Ransack the description for possible datetime objects.  If we find one
        # then we set start_date as that found datetime.
        for word in event.description.split():
            try:
                guessed_date = parse(word)
                break
            except ValueError:
                continue
        event.start_date = guessed_date
        event.save()
        if 'next' in request.POST:
            next = request.POST['next']
        else:
            next = reverse('ev_tonight')
        if request.is_ajax():
            # If the request is AJAX, then render the created event and don't
            # create messages for the user.
            try:
                Attendance.objects.get(event=event, user=request.user)
                attending = True
            except Attendance.DoesNotExist:
                attending = False
            return render_to_response('events/event.html', {'event': event,
                'request': request, 'attending': attending, 
                'authenticated': True, 'event_num': 1, 'next': next})
        else:
            # If the request is not AJAX, then create messages for the user and
            # redirect them to the next page.
            request.user.message_set.create(
                message=_('Your event was posted.'))
            return HttpResponseRedirect(next)
    if request.is_ajax():
        raise Http404
    return render_to_response(
        'events/create.html',
        {'form': form},
        context_instance = RequestContext(request)
    )
create = login_required(create)

def toggle_attendance(request):
    """
    Toggles whether a user is set to attend an event or not.
    """
    try:
        event_id = int(request.POST['event_id'])
    except (KeyError, ValueError):
        raise Http404
    event = get_object_or_404(Event, id=event_id)
    attendance, created = Attendance.objects.get_or_create(user=request.user, 
        event=event)
    if not created:
        attendance.delete()
    if request.is_ajax():
        # If the request is AJAX, return JSON representing the new count of
        # people who are attending the event.
        json = '{"created": %s, "count": %s}' % (created and 'true' or 'false', 
            event.attendees.all().count())
        return HttpResponse(json, mimetype='application/json')
    # If the request was not AJAX, create messages for the user.
    if created:
        request.user.message_set.create(
            message=_('You are now attending "%s"') % unicode(event))
    else:
        request.user.message_set.create(
            message=_('You are no longer attending "%s"') % unicode(event))
    next = request.POST.get('next', '')
    #if not next:
    #    next = reverse('ev_tonight')
    return HttpResponseRedirect(next)
toggle_attendance = require_POST(login_required(toggle_attendance))