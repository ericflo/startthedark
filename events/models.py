from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

class EventQuerySet(QuerySet):
    def today(self):
        now = datetime.now()
        start = datetime.min.replace(year=now.year, month=now.month,
            day=now.day)
        end = (start + timedelta(days=1)) - timedelta.resolution
        return self.filter(creation_date__range=(start, end))

class EventManager(models.Manager):
    def get_query_set(self):
        return EventQuerySet(self.model)
    
    def today(self):
        return self.get_query_set().today()

class Event(models.Model):
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User, related_name='event_creator_set')
    attendees = models.ManyToManyField(User, through='Attendance')
    latest = models.BooleanField(default=True)
    
    objects = EventManager()
    
    def __unicode__(self):
        if len(self.description) > 80:
            return self.description[:76] + ' ...'
        return self.description[:80]
    
    def save(self, **kwargs):
        Event.objects.today().filter(creator=self.creator).update(latest=False)
        super(Event, self).save(**kwargs)
    
    def description_size(self):
        if len(self.description) < 120:
            return 'small'
        elif len(self.description) < 240:
            return 'medium'
        else:
            return 'large'

class Attendance(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    registration_date = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return "%s is attending %s" % (self.user.username, self.event)
    
    class Meta(object):
        verbose_name_plural = "Attendance"
