from django.conf import settings

def production(request):
    if not settings.DEBUG:
        return {'MEDIA_SUFFIX': '-prod'}
    return {}