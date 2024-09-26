from django.views.generic import ListView

from .models import RemarkableEvent


class TwentyYearsAnniversaryView(ListView):
    queryset = RemarkableEvent.objects.order_by("-date")
    template_name = "anniversaries/20.html"
    context_object_name = "events"
