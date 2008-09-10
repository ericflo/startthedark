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

def events(request, template_name='tonight.html', today=True, all_events=False):
    events = Event.objects.filter(latest=True).order_by('-creation_date')
    following = []
    if request.user.is_authenticated():
        my_events = Event.objects.filter(latest=True)
        my_events = my_events.filter(creator=request.user) | my_events.filter(
            attendance__user=request.user)
        events = events.exclude(creator=request.user)
        events = events.exclude(attendance__user=request.user)
        if not all_events:
            following = request.user.following_set.all().values('to_user')
            events = events.filter(creator__in=[i['to_user'] for i in following]) | \
                events.filter(attendance__user__in=[i['to_user'] for i in following])
    else:
        my_events = Event.objects.none()
    if today:
        events = events.today().order_by('-start_date')
        try:
            my_events = my_events.today()
        except AttributeError:
            pass
    context = {
        'events': events,
        'my_events': my_events,
        'following': following,
        'event_form': EventForm(),
        'today': today,
        'all_events': all_events,
    }
    return render_to_response(
        'events/%s' % template_name,
        context,
        context_instance = RequestContext(request)
    )

def event(request, id):
    event = get_object_or_404(Event, id=id)
    return render_to_response(
        'events/event_details.html',
        {'event': event},
        context_instance = RequestContext(request)
    )

def create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.creator = request.user
        guessed_date = None
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
            try:
                Attendance.objects.get(event=event, user=request.user)
                attending = True
            except Attendance.DoesNotExist:
                attending = False
            return render_to_response('events/event.html', {'event': event,
                'request': request, 'attending': attending, 
                'authenticated': True, 'event_num': 1, 'next': next})
        else:
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
        json = '{"created": %s, "count": %s}' % (created and 'true' or 'false', 
            event.attendees.all().count())
        return HttpResponse(json, mimetype='application/json')
    if created:
        request.user.message_set.create(
            message=_('You are now attending "%s"') % unicode(event))
    else:
        request.user.message_set.create(
            message=_('You are no longer attending "%s"') % unicode(event))
    next = request.POST.get('next', '')
    #if not next:
    #    next = reverse('ev_tonight')
    print "Redirecting to %s" % next
    return HttpResponseRedirect(next)
toggle_attendance = require_POST(login_required(toggle_attendance))