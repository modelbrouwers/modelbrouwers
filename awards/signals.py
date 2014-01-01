from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Vote, FIELD_2_POINTS


@receiver(post_save, sender=Vote)
def update_points(sender, **kwargs):
    """ On creation of the Vote, set the points for the project """
    if kwargs['created']:
        vote = kwargs.get('instance')
        for field, _points in FIELD_2_POINTS.items():
            project = getattr(vote, field, None)
            if project:
                project.votes = F('votes') + _points
                project.save()
