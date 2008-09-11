from django.conf import settings

class Counter(object):
    """
    A simple counter class which keeps a single integer as private state.  Every
    time ``get_int`` is called, that integer is returned and then incremented
    internally by one.
    """
    i = 1
    
    def get_int(self):
        self.i += 1
        return self.i - 1

def production(request):
    """
    Serves two purposes:
    
    1. To simply put one instance of ``Counter`` into the context for use
       anywhere within the site.
       
    2. To conditionally set a 'MEDIA_SUFFIX' context variable with the value
       '-prod'.  This is used for media files that differ from development to
       production.
    """
    context = {'counter': Counter()}
    if not settings.DEBUG:
        context['MEDIA_SUFFIX'] = '-prod'
    return context