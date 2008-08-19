import datetime

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name='event_creator_set')
    attendees = models.ManyToManyField(User, through='Attendance')
    
    def __unicode__(self):
        return self.description[:140]

class Attendance(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    registration_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return "%s is attending %s" % (self.user.username, self.event)
    
    class Meta(object):
        verbose_name_plural = "Attendance"