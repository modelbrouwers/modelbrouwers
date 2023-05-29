from typing import Literal

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView


class DevViewMixin(LoginRequiredMixin, UserPassesTestMixin):  # pragma: no cover
    """
    Mixin to allow view access only in dev mode.
    """

    request: HttpRequest

    def test_func(self):
        return settings.DEBUG and self.request.user.is_superuser


class EmailDebugViewMixin:  # pragma: no cover
    """
    Mixin to view the contents of an e-mail as they would be sent out.

    This view supports ?mode=html|text querystring param, defaulting to HTML.
    """

    template_name = "emails/wrapper.html"
    request: HttpRequest

    def _get_mode(self) -> Literal["text", "html"]:
        mode = self.request.GET.get("mode", "html")
        assert mode in ("html", "text"), f"Unknown mode: {mode}"
        return mode

    def get_email_content(self):
        raise NotImplementedError()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        content = self.get_email_content()
        ctx.update(
            {
                **kwargs,
                "main_website_url": self.request.build_absolute_uri(
                    reverse("shop:index")
                ),  # TODO -> setting/config?
                "content": content,
            }
        )
        return ctx

    def render_to_response(self, context, **response_kwargs):
        mode = self._get_mode()
        if mode == "text":
            return HttpResponse(
                context["content"].encode("utf-8"), content_type="text/plain"
            )
        return super().render_to_response(context, **response_kwargs)


class EmailWrapperTestView(
    DevViewMixin, EmailDebugViewMixin, TemplateView
):  # pragma: no cover
    def get_email_content(self):
        content = "<b>content goes here</b>"
        return mark_safe(content)
