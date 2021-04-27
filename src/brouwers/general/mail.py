"""
Easy sending of ``EmailMultiAlternatives`` emails.
"""
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class MultiAlternativesEmail(object):
    """CBV approach for MultiAlternativesEmail"""

    template_name = None
    subject = None
    to = None
    msg = None

    def __init__(self, to=None, **kwargs):
        self.to = to
        self.kwargs = kwargs or {}

    def get_template(self, content="html"):
        """
        Returns a list of template names to be used for the request. Must return
        a list.

        :param content: either 'html' or 'txt'.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "MultiAlternativesEmail requires either a definition of "
                "'template_name' or an implementation of 'get_template'"
            )
        else:
            template_name = "%s.%s" % (self.template_name, content)
            return get_template(template_name)

    def get_subject(self):
        if self.subject is None:
            raise ImproperlyConfigured(
                "MultiAlternativesEmail requires either a definition of "
                "'subject' or an implementation of 'get_subject'"
            )
        return self.subject

    def get_to(self):
        if self.to is None:
            raise ImproperlyConfigured(
                "MultiAlternativesEmail requires either a definition of "
                "'to' or an implementation of 'get_to'"
            )
        # iterable and not string
        if isinstance(self.to, (tuple, list)):
            return self.to
        return [self.to]

    def get_context_data(self, **kwargs):
        kwargs.update(**{"site": Site.objects.get_current()})
        return kwargs

    def get_text_content(self):
        template = self.get_template(content="txt")
        context = self.get_context_data(**self.kwargs)
        return template.render(context)

    def get_html_content(self):
        template = self.get_template(content="html")
        context = self.get_context_data(**self.kwargs)
        return template.render(context)

    def get_email(self):
        """Get a EmailMessage instance"""
        to = self.get_to()
        subject = self.get_subject()

        text_content = self.get_text_content()
        html_content = self.get_html_content()

        msg = EmailMultiAlternatives(subject, text_content, to=to)
        msg.attach_alternative(html_content, "text/html")
        self.msg = msg
        return msg

    def send(self, fail_silently=False):
        if not self.msg:
            self.get_email()
        self.msg.send(fail_silently=fail_silently)
