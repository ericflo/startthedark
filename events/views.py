from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Event, Attendance

def tonight(self):
    pass
tonight = login_required(tonight)