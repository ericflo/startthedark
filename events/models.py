from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

def today():
    """
    Returns a tuple of two datetime instances: the beginning of today, and the 
    end of today.
    """
    now = datetime.now()
    start = datetime.min.replace(year=now.year, month=now.month,
        day=now.day)
    end = (start + timedelta(days=1)) - timedelta.resolution
    return (start, end)

class EventQuerySet(QuerySet):
    """
    A very simple ``QuerySet`` subclass which adds only one extra method,
    ``today``, which returns only those objects whose ``creation_date`` falls
    within the bounds of today.
    """
    def today(self):
        """
        Filters down to only those objects whose ``creation_date`` falls within
        the bounds of today.
        """
        return self.filter(creation_date__range=today())

class EventManager(models.Manager):
    """
    A very simple ``Manager`` subclass which returns an ``EventQuerySet``
    instead of the typical ``QuerySet``.  It also includes a proxy for the extra
    ``today`` method that is provided by the ``EventQuerySet`` subclass.
    """
    def get_query_set(self):
        """
        Gets an ``EventQuerySet`` instead of a typical ``QuerySet``.
        """
        return EventQuerySet(self.model)
    
    def today(self):
        """
        A proxy method for the extra ``today`` method that is provided by the
        ``EventQuerySet`` subclass.
        """
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
        """
        Returns the first 80 characters of the description, or less, if the
        description is less than 80 characters.
        """
        if len(self.description) > 80:
            return self.description[:76] + ' ...'
        return self.description[:80]
    
    def save(self, **kwargs):
        """
        First this updates all events created today by the same creator as this
        event, and sets their ``latest`` field to False.
        
        Then, this simply saves the object.  Since the default for ``latest`` is
        to be set to True, it will be passed through and saved as the latest
        event for today by this user.
        """
        Event.objects.today().filter(creator=self.creator).update(latest=False)
        super(Event, self).save(**kwargs)
    
    def today(self):
        """
        Determines whether this event takes place today or not.
        """
        (start, end) = today()
        return self.creation_date >= start and self.creation_date <= end
    
    def description_size(self):
        """
        Useful only for display purposes, this designates a label of 'small',
        'medium', or 'large' to the description text size.
        """
        if len(self.description) < 120:
            return 'small'
        elif len(self.description) < 240:
            return 'medium'
        else:
            return 'large'

class Attendance(models.Model):
    """
    This is the explicit intermediary model mapping ``User`` instances to
    ``Event`` instances.
    """
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    registration_date = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return "%s is attending %s" % (self.user.username, self.event)
    
    class Meta(object):
        verbose_name_plural = "Attendance"
