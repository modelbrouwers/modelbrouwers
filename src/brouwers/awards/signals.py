from django.db.models import F
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from brouwers.general.models import UserProfile

from .models import FIELD_2_POINTS, Project, Vote


@receiver(post_init, sender=UserProfile)
def set_awards_preferences(sender, **kwargs):
    profile = kwargs.get('instance')
    profile._exclude_from_nomination = profile.exclude_from_nomination


@receiver(post_save, sender=UserProfile)
def deactivate_awards(sender, **kwargs):
    if kwargs.get('raw') or kwargs.get('created'):
        return

    profile = kwargs.get('instance')
    if profile is None:
        return

    if profile.exclude_from_nomination and profile._exclude_from_nomination is False:
        Project.objects.filter(brouwer__iexact=profile.user.username).update(rejected=True)


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
