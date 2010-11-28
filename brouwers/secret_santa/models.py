from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
	user = models.ForeignKey(User)
	year = models.CharField(max_length=4)
	verified = models.BooleanField()
	
	def __unicode__(self):
		return self.user.get_profile().forum_nickname

class Couple(models.Model):
	sender = models.ForeignKey(Participant)
	receiver = models.ForeignKey(Participant, related_name='receiver')
	
	def __unicode__(self):
		return ("%s - %s" % (self.sender.__unicode__(), self.receiver.__unicode__()))
