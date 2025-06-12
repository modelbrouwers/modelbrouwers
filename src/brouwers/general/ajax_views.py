from django.http import JsonResponse
from django.views.generic.base import View

from .models import Announcement


class AnnouncementView(View):
    def get(self, request, *args, **kwargs):
        data = {"html": None}
        announcement = Announcement.objects.get_current()
        if announcement is not None:
            data["html"] = announcement.text
        return JsonResponse(data)
