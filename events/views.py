from datetime import datetime, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from events.models import Event, Attendance

def events(request, template_name='tonight.html', today=True, all_events=False):
    events = Event.objects.all()
    if not all_events:
        following = request.user.following_set.all().values('to_user')
        events = events.filter(creator__in=[i['to_user'] for i in following])
    if today:
        now = datetime.now()
        today_start = datetime.min.replace(year=now.year, month=now.month,
            day=now.day)
        today_end = (today_start + timedelta(days=1)) - timedelta.resolution
        events = events.filter(start_date__range=(today_start, today_end))
    context = {
        'events': events,
    }
    return render_to_response(
        'events/%s' % template_name,
        context,
        context_instance = RequestContext(request)
    )