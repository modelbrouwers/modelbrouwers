from django.db.models.signals import post_save
from django.dispatch import receiver

from general.models import UserProfile
from .models import User


@receiver(post_save, sender=User)
def create_userprofile(sender, **kwargs):
    if kwargs.get('created') and not kwargs.get('raw'):
        user = kwargs.get('instance')
        fields = {
            'user': user,
            'forum_nickname': user.username,
        }
        UserProfile.objects.create(**fields)

@receiver(post_save, sender=User)
def sync_email(sender, **kwargs):
    if not kwargs.get('raw'):
        user = kwargs.get('instance')
        forum_user = user.forumuser
        if forum_user and user.email != forum_user.user_email:
            forum_user.user_email = user.email
            forum_user.save()

@receiver(post_save, sender=User)
def sync_userprofile(sender, **kwargs):
    if not kwargs.get('raw'):
        user = kwargs.get('instance')
        profile = user.profile
        if not kwargs.get('created') and profile.forum_nickname != user.username:
            profile.forum_nickname = user.username
            profile.save()

@receiver(post_save, sender=User)
def sync_forumuser_username(sender, **kwargs):
    if not kwargs.get('raw'):
        user = kwargs.get('instance')
        forum_user = user.forumuser
        if forum_user and user.username != forum_user.username:
            forum_user.username = user.username
            forum_user.save()
