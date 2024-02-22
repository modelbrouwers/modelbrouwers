from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .models import ContactMessage


class ContactMessageCreateView(SuccessMessageMixin, CreateView):
    model = ContactMessage
    fields = ("name", "email", "message")
    success_url = reverse_lazy("contact")
    success_message = _(
        "Thank you for your message, we will get back to you as soon as possible."
    )

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        transaction.on_commit(lambda: self.object.notify_creation())
        return response
