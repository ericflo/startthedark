import os, sys
sys.stdout = sys.stderr

if '/var/www/startthedark.com' not in sys.path:
    sys.path.append('/var/www/startthedark.com')
if '/var/www/startthedark.com/startthedark' not in sys.path:
    sys.path.append('/var/www/startthedark.com/startthedark')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
