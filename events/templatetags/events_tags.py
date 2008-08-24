from django import template
from events.models import Attendance

def event(context, e):
    try:
        Attendance.objects.get(event=e, user=context['user'])
        attending = True
    except Attendance.DoesNotExist:
        attending = False
    return {
        'event': e,
        'attending': attending,
        'request': context['request'],
    }

register = template.Library()
register.inclusion_tag('events/event.html', takes_context=True)(event)