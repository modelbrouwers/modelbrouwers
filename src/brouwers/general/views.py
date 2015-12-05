from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views.generic import View

from .forms import *


EMPTY_CONTEXT = {}

User = get_user_model()


def index(request):
    if request.GET.get('django') or settings.DEBUG:
        return render(request, 'base.html')
    return HttpResponseRedirect('/index.php')


@login_required
def profile(request):
    return redirect('users:profile')


class ServeHbsTemplateView(View):
    def get(self, request, *args, **kwargs):
        app_name = kwargs.get('app_name')
        template_name = "{template_name}.hbs".format(template_name=kwargs.get('template_name'))

        template_path = "{app_name}/handlebars/{template_name}".format(
                            app_name=app_name,
                            template_name=template_name
                        )
        template = get_template(template_path)
        tpl_source = template.render(EMPTY_CONTEXT)
        return HttpResponse(tpl_source)
