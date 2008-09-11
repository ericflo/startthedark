from django import template
from django.template.defaultfilters import stringfilter
from events.models import Attendance

def event(context, e, event_num=1):
    """
    Renders a single ``Event`` object.
    """
    to_return = {
        'event': e,
        'request': context['request'],
        'event_num': event_num,
    }
    if context['user'].is_authenticated():
        # If the user is authenticated, check if he/she is attending the event.
        try:
            Attendance.objects.get(event=e, user=context['user'])
            attending = True
        except Attendance.DoesNotExist:
            attending = False
        to_return.update({
            'attending': attending,
            'authenticated': True,
        })
    else:
        to_return.update({'authenticated': False})
    return to_return

def truncate(input_str, arg):
    """
    Truncates a string of characters to a certain length, eliding as necessary.
    """
    try:
        input_str = unicode(input_str)
        arg = int(arg)
    except ValueError:
        return input_str
    if len(input_str) > arg:
        return input_str[:arg-3] + '...'
    return input_str
truncate = stringfilter(truncate)

register = template.Library()
register.filter('truncate', truncate)
register.inclusion_tag('events/event.html', takes_context=True)(event)