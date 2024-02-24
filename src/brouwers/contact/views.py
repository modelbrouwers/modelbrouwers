from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from brouwers.legacy_shop.models import OcSetting

from .forms import ContactMessageForm
from .models import ContactMessage


class ContactMessageCreateView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    success_url = reverse_lazy("contact")
    success_message = _(
        "Thank you for your message, we will get back to you as soon as possible."
    )

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object: ContactMessage
        transaction.on_commit(lambda: self.object.notify_creation())
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        details = {
            setting.key.removeprefix("config_"): setting.value
            for setting in OcSetting.objects.filter(
                group="config", key__in=["config_telephone", "config_address"]
            )
        }
        context["contact_details"] = details
        return context
