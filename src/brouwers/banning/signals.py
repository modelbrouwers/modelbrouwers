from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from models import Ban
from utils import set_banning_cache


@receiver(post_delete, sender=Ban)
@receiver(post_save, sender=Ban)
def update_bans_cache(sender, **kwargs):
    """ Ban added or deleted, add it to the cache """
    set_banning_cache()
