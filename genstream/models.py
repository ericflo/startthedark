from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class StreamItem(models.Model):
    user = models.ForeignKey(User)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    date = models.DateTimeField()
    is_new = models.BooleanField(default=True)
    
    def __unicode__(self):
        return unicode(self.content_object)
    
    class Meta:
        unique_together = (('user', 'object_id', 'content_type'),)