import random
import hashlib
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader, Context
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.utils import timezone

from .forms import *
from .models import Redirect, PasswordReset


LOG_REGISTRATION_ATTEMPTS = getattr(settings, 'LOG_REGISTRATION_ATTEMPTS', True)

EMPTY_CONTEXT = Context()

User = get_user_model()


######## EMAIL TEMPLATES ############
TEMPLATE_RESET_PW_HTML = """
    <p>Hello %(nickname)s,</p><br >
    <p>You (or someone else) has requested a password reset
    for your account at Modelbrouwers.nl. This request will
    expire after 24 hours.</p><br >
    <p>You can reset your password on the following url: <a href="%(url)s">%(url)s</a>
    </p>
    <br ><br >
    <p>Sincerely,</p>
    <p>The administrators of Modelbrouwers.nl</p>
"""


def index(request):
    if request.GET.get('django') or settings.DEBUG:
        return render(request, 'base.html')
    return HttpResponseRedirect('/index.php')


#############################
#    showing userprofile    #
#############################

@login_required
def profile(request):
    return redirect('users:profile')


def test_redirects(request, path):
    redirect = get_object_or_404(Redirect, path_from__iexact=path)
    return HttpResponseRedirect(redirect.path_to)


class ServeHbsTemplateView(View):
    def get(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name')
        template_name = "{template_name}.hbs".format(template_name=kwargs.get('template_name'))

        template_path = "{app_name}/handlebars/{template_name}".format(
                            app_name=app_name,
                            template_name=template_name
                        )
        template = loader.get_template(template_path)
        tpl_source = template.render(EMPTY_CONTEXT)
        return HttpResponse(tpl_source)
