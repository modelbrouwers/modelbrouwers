from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from .models import RemarkableEvent


class TwentyYearsAnniversaryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = RemarkableEvent.objects.order_by("-date")
    template_name = "anniversaries/20.html"
    context_object_name = "events"

    def test_func(self):
        return self.request.user.is_superuser
