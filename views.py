from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('ev_tonight'))
    return direct_to_template(request, template='index.html')