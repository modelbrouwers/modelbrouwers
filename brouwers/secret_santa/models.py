from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
	user = models.ForeignKey(User)
	year = models.CharField(max_length=4)
