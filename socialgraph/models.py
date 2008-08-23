import datetime

from django.contrib.auth.models import User

class UserLink(models.Model):
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)
    date_added = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return "%s is following %s" % (self.from_user.username, 
            self.to_user.username)

    def save(self):
        if from_user == to_user:
            raise ValueError("Cannot follow yourself.")
        super(UserLink, self).save()
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)