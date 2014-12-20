from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import GroupBuild


@receiver(m2m_changed, sender=GroupBuild, dispatch_uid='set-applicant-admin')
def add_applicant_to_admins(sender, **kwargs):
    gb = kwargs['instance']
    if gb._created and gb.applicant not in gb.admins.all():
        gb.admins.add(gb.applicant)
