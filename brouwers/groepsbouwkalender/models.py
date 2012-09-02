from django.contrib.auth.models import User
from django.db import models

# Create your models here.
FORUMGEDEELTE_CHOICES = (
    ('g','ter land'),
    ('l','ter lucht'),
    ('z','ter zee'),
    ('a', 'anders'),
)

STATUS_CHOICES = (
    ('a','aangevraagd'),
    ('l','lopend'),
    ('g','goedgekeurd'),
    ('d','afgekeurd'),
)
    
DURATION_CHOICES = (
    (1,'1 maand'),
    (2,'2 maanden'),
    (3,'3 maanden'),
    (6,'6 maanden'),
    (12,'12 maanden'),
)
    
class Groepsbouw(models.Model):
    applicant = models.ForeignKey(User)
    #TODO applicant mag veranderen naar een ForeignKey naar User. vergelijk met albums/models.py op lijn 35 en zie ook lijn 4
    buildname = models.CharField(max_length=200, unique=False)
    forumpart = models.CharField(max_length=1, choices=FORUMGEDEELTE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.PositiveSmallIntegerField(default=6, choices=DURATION_CHOICES)
    description = models.TextField(blank=True)
    topiclink = models.URLField(max_length=500)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    opmerkingen = models.CharField(max_length=300, blank=True)

    
