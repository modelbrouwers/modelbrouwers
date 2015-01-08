import random
import hashlib
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader, Context
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.utils import timezone

from brouwers.albums.models import Album
from brouwers.albums.utils import admin_mode
from .forms import *
from .models import UserProfile, Redirect, PasswordReset


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

# FIXME use django built ins
def password_reset(request):
    if request.method == "POST":
        form = RequestPasswordResetForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.warning(request, _("Your account is still inactive! You won't be able to log in until you reactivate with the link sent by e-mail."))
            expire = timezone.now() + timedelta(days=1)
            variable_part = expire.strftime("%Y-%m-%d %H:%M:%S") + str(int(random.random() * 10))
            h = hashlib.sha1("%s%s" % (settings.SECRET_KEY, variable_part)).hexdigest()[:24]

            # make sure the hash is unique enough
            reset = PasswordReset(user=user, expire=expire, h=h)
            try:
                reset.save()
            except IntegrityError:
                extrapart = int(random.random() * 10)
                h = hashlib.sha1("%s%s%s" % (settings.SECRET_KEY, variable_part, extrapart)).hexdigest()[:24]
                reset = PasswordReset(user=user, expire=expire, h=h)
                reset.save()

            #send email
            nickname = user.username
            email = user.email
            if not email:
                email = 'admins@modelbrouwers.nl'
            domain = Site.objects.get_current().domain
            url = "http://%s%s?h=%s" % (
                    domain,
                    reverse(do_password_reset),
                    h
                    )

            text_content = _("""Hello %(nickname)s, \n
You or someone else has requested a password reset for your Modelbrouwers.nl account.
This request will expire after 24 hours.\n
Go to %(url)s to complete your password reset.\n
Sincerely,\n
The Modelbrouwers.nl staff""" % {
                                'nickname': nickname,
                                'url': url
                                }
                            )

            html_content = _(TEMPLATE_RESET_PW_HTML % {
                                'nickname': nickname,
                                'url': url
                                }
                            )
            subject, from_email = _("Modelbrouwers.nl password reset"), 'admins@modelbrouwers.nl'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, _("An e-mail was sent to '%(email)s' with a link to reset your pasword.") % {'email': email})
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = RequestPasswordResetForm()
    return render(request, 'general/password_reset.html', {'form': form})

def do_password_reset(request):
    if request.method == "POST":
        hashform = HashForm(request.POST)
        form = PasswordResetForm(request.POST)
        if hashform.is_valid():
            h = hashform.cleaned_data['h']
            pr = get_object_or_404(PasswordReset, h=h)
            if form.is_valid():
                user = form.cleaned_data['user']
                if user == pr.user:
                    pw = form.cleaned_data['password1']
                    user.set_password(pw)
                    user.save()
                    pr.delete()
                    return HttpResponseRedirect(reverse('users:login'))
                else:
                    pass #TODO: messages tonen & loggen
    else:
        hashform = HashForm(request.GET)
        form = None
        if hashform.is_valid():
            h = hashform.cleaned_data['h']
            pr = get_object_or_404(PasswordReset, h=h)
            form = PasswordResetForm(initial={'user': pr.user})
    return render(request, 'general/do_password_reset.html', {'form': form, 'hashform': hashform})


class ServeHbsTemplateView(View):
    def get(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name')
        template_name = "{template_name}.hbs".format(template_name=kwargs.get('template_name'))

        template_path = "{app_name}/handlebars/{template_name}".format(
                            app_name = app_name,
                            template_name = template_name
                        )
        template = loader.get_template(template_path)
        tpl_source = template.render(EMPTY_CONTEXT)
        return HttpResponse(tpl_source)
