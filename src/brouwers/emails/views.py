from typing import Literal

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import View


class DevViewMixin(LoginRequiredMixin, UserPassesTestMixin):  # pragma: no cover
    """
    Mixin to allow view access only in dev mode.
    """

    request: HttpRequest

    def test_func(self):
        return settings.DEBUG and self.request.user.is_superuser


class BaseEmailDebugView(DevViewMixin, View):  # pragma: no cover
    """
    Mixin to view the contents of an e-mail as they would be sent out.

    This view supports ?mode=html|text querystring param, defaulting to HTML.
    """

    template_name = "emails/wrapper.html"

    def _get_mode(self) -> Literal["text", "html"]:
        mode = self.request.GET.get("mode", "html")
        assert mode in ("html", "text"), f"Unknown mode: {mode}"
        return mode

    def get_email_content(self, mode: Literal["text", "html"]):
        raise NotImplementedError()

    def get(self, request: HttpRequest, *args, **kwargs):
        mode = self._get_mode()
        content = self.get_email_content(mode)
        if mode == "text":
            content_type = "text/plain; charset=utf-8"
        elif mode == "html":
            content_type = "text/html"
        else:
            raise ValueError("Unsupported mode")
        return HttpResponse(content.encode("utf-8"), content_type=content_type)


class EmailWrapperTestView(BaseEmailDebugView):  # pragma: no cover
    def get_email_content(self, mode: Literal["text", "html"]) -> str:
        template = loader.get_template("emails/wrapper.html")
        context = {
            "base": self.request.build_absolute_uri(reverse("index")),
        }
        return template.render(context)
