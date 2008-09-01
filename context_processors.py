from django.conf import settings

class Counter(object):
    i = 1
    
    def get_int(self):
        self.i += 1
        return self.i - 1

def production(request):
    context = {'counter': Counter()}
    if not settings.DEBUG:
        context['MEDIA_SUFFIX'] = '-prod'
    return context