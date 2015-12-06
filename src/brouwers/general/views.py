from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View

from .forms import *


EMPTY_CONTEXT = {}

User = get_user_model()


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
